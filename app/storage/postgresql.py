from __future__ import annotations

import json
import re
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any


try:
    import psycopg
    from psycopg.types.json import Jsonb
    from psycopg.rows import dict_row
except ModuleNotFoundError:  # pragma: no cover - exercised in minimal local envs
    psycopg = None  # type: ignore[assignment]
    Jsonb = None  # type: ignore[assignment]
    dict_row = None  # type: ignore[assignment]


BOOLEAN_CONSTANTS = (
    (re.compile(r"\bis_read\s*=\s*0\b"), "is_read = FALSE"),
    (re.compile(r"\bis_read\s*=\s*1\b"), "is_read = TRUE"),
    (re.compile(r"\binventory_lock\s*=\s*0\b"), "inventory_lock = FALSE"),
    (re.compile(r"\bis_active\s*=\s*0\b"), "is_active = FALSE"),
    (re.compile(r"\bis_active\s*=\s*1\b"), "is_active = TRUE"),
    (re.compile(r"\binventory_lock\s*=\s*1\b"), "inventory_lock = TRUE"),
)

BOOLEAN_PARAM_COLUMNS = {
    "inventory_lock",
    "is_controlled",
    "quarantine",
    "is_read",
    "is_preferred",
    "is_active",
}

JSONB_PARAM_COLUMNS = {
    "audit_log": {"payload"},
    "marketplace_payments": {"metadata"},
    "marketplace_payment_events": {"payload"},
}


class PostgresDatabase:
    def __init__(self, database_url: str) -> None:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL runtime")
        self.database_url = normalize_psycopg_url(database_url)

    def connect(self) -> "PostgresConnection":
        raw_connection = psycopg.connect(self.database_url, row_factory=dict_row)
        return PostgresConnection(raw_connection)

    def init_schema(self) -> None:
        # PostgreSQL schema is managed by Alembic, not by runtime startup.
        return None

    @contextmanager
    def transaction(self) -> Iterator["PostgresConnection"]:
        connection = self.connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()


class PostgresConnection:
    dialect = "postgresql"

    def __init__(self, connection: Any) -> None:
        self._connection = connection

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> Any:
        translated_query = translate_sqlite_query(query)
        translated_params = adapt_params_for_query(translated_query, params)
        return self._connection.execute(translated_query, translated_params)

    def insert_and_get_id(self, query: str, params: tuple[Any, ...]) -> int:
        translated_query = translate_sqlite_query(query).rstrip()
        if " returning " not in translated_query.lower():
            translated_query = f"{translated_query} RETURNING id"
        translated_params = adapt_params_for_query(translated_query, params)
        row = self._connection.execute(translated_query, translated_params).fetchone()
        if row is None:
            raise RuntimeError("PostgreSQL INSERT did not return an id")
        return int(row["id"])

    def executescript(self, _script: str) -> None:
        raise RuntimeError("PostgreSQL runtime schema is managed by Alembic")

    def commit(self) -> None:
        self._connection.commit()

    def rollback(self) -> None:
        self._connection.rollback()

    def close(self) -> None:
        self._connection.close()


def translate_sqlite_query(query: str) -> str:
    translated = _replace_placeholders(query)
    for pattern, replacement in BOOLEAN_CONSTANTS:
        translated = pattern.sub(replacement, translated)
    return translated


def normalize_psycopg_url(database_url: str) -> str:
    if database_url.startswith("postgresql+psycopg://"):
        return "postgresql://" + database_url.removeprefix("postgresql+psycopg://")
    return database_url


def adapt_params_for_query(query: str, params: tuple[Any, ...]) -> tuple[Any, ...]:
    if not params:
        return params
    normalized_query = " ".join(query.lower().split())
    params = _adapt_jsonb_params(normalized_query, params)
    boolean_param_indexes = _boolean_param_indexes(normalized_query)
    if not boolean_param_indexes:
        return params
    adapted = list(params)
    for index in boolean_param_indexes:
        if index < len(adapted) and adapted[index] in (0, 1):
            adapted[index] = bool(adapted[index])
    return tuple(adapted)


def _adapt_jsonb_params(query: str, params: tuple[Any, ...]) -> tuple[Any, ...]:
    if Jsonb is None:
        return params
    jsonb_indexes = _insert_jsonb_param_indexes(query)
    if not jsonb_indexes:
        return params
    adapted = list(params)
    for index in jsonb_indexes:
        if index >= len(adapted):
            continue
        payload = adapted[index]
        if isinstance(payload, str):
            payload = json.loads(payload)
        adapted[index] = Jsonb(payload)
    return tuple(adapted)


def _replace_placeholders(query: str) -> str:
    result: list[str] = []
    in_single_quote = False
    in_double_quote = False
    for char in query:
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            result.append(char)
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            result.append(char)
        elif char == "?" and not in_single_quote and not in_double_quote:
            result.append("%s")
        else:
            result.append(char)
    return "".join(result)


def _boolean_param_indexes(query: str) -> set[int]:
    insert_indexes = _insert_boolean_param_indexes(query)
    if insert_indexes:
        return insert_indexes

    indexes: set[int] = set()
    params_seen = 0
    tokens = re.split(r"(%s)", query)
    prefix = ""
    for token in tokens:
        if token == "%s":
            if _placeholder_targets_boolean(prefix):
                indexes.add(params_seen)
            params_seen += 1
            prefix = ""
        else:
            prefix = (prefix + token)[-160:]
    return indexes


def _placeholder_targets_boolean(prefix: str) -> bool:
    return any(re.search(rf"\b{column}\b\s*=\s*$", prefix) for column in BOOLEAN_PARAM_COLUMNS) or any(
        re.search(rf"\b{column}\b[^,)]*,\s*$", prefix) for column in BOOLEAN_PARAM_COLUMNS
    )


def _insert_boolean_param_indexes(query: str) -> set[int]:
    return _insert_column_param_indexes(query, BOOLEAN_PARAM_COLUMNS)


def _insert_jsonb_param_indexes(query: str) -> set[int]:
    match = re.search(
        r"\binsert\s+into\s+(?P<table>\w+)\s*\((?P<columns>.*?)\)\s*values\s*\((?P<values>.*?)\)",
        query,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match is None:
        return set()
    table = _normalize_identifier(match.group("table"))
    columns = JSONB_PARAM_COLUMNS.get(table)
    if not columns:
        return set()
    return _insert_column_param_indexes(query, columns)


def _insert_column_param_indexes(query: str, target_columns: set[str]) -> set[int]:
    match = re.search(
        r"\binsert\s+into\s+\w+\s*\((?P<columns>.*?)\)\s*values\s*\((?P<values>.*?)\)",
        query,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match is None:
        return set()

    columns = [_normalize_identifier(column) for column in _split_sql_list(match.group("columns"))]
    values = _split_sql_list(match.group("values"))
    indexes: set[int] = set()
    param_index = 0
    for column, value in zip(columns, values, strict=False):
        placeholders = value.count("%s")
        if placeholders and column in target_columns:
            indexes.add(param_index)
        param_index += placeholders
    return indexes


def _split_sql_list(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    in_single_quote = False
    in_double_quote = False
    depth = 0
    for char in value:
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif char == "(" and not in_single_quote and not in_double_quote:
            depth += 1
        elif char == ")" and not in_single_quote and not in_double_quote and depth:
            depth -= 1
        if char == "," and not in_single_quote and not in_double_quote and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    if current:
        parts.append("".join(current).strip())
    return parts


def _normalize_identifier(value: str) -> str:
    return value.strip().strip('"').split(".")[-1]
