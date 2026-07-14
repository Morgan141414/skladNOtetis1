from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sklad Service"
    deployment_mode: Literal["demo", "staging", "production"] = "demo"
    database_backend: Literal["sqlite", "postgresql"] = "sqlite"
    database_url: str = "sqlite:///./sklad.db"
    public_access_enabled: bool = True
    production_public_access_acknowledged: bool = False
    dev_auth_enabled: bool = False
    jwt_hmac_secret: str | None = None
    jwt_algorithm: Literal["HS256"] = "HS256"
    jwt_issuer: str | None = None
    jwt_audience: str | None = None
    jwt_clock_skew_seconds: int = 30
    background_jobs_enabled: bool = False
    background_jobs_interval_seconds: int = 3600
    background_jobs_expiry_days: int = 30
    background_jobs_actor_id: str = "system-scheduler"
    oidc_enabled: bool = False
    oidc_discovery_url: str | None = None  # e.g. https://keycloak.host/realms/tetis/.well-known/openid-configuration
    oidc_audience: str | None = None
    oidc_issuer: str | None = None
    oidc_role_mapping_json: str | None = None  # JSON: {"keycloak-role": "sklad-role"}
    anthropic_api_key: str | None = None
    accounting_webhook_url: str | None = None
    accounting_webhook_secret: str | None = None
    grafana_webhook_token: str | None = None
    mis_webhook_url: str | None = None
    mis_api_key: str | None = None
    mis_inbound_webhook_token: str | None = None
    mis_sso_secret: str | None = None  # shared with MIS's SKLAD_SSO_SECRET, for embedding sklad in the MIS sidebar
    cameras_sso_secret: str | None = None  # shared with cameras backend CAMERAS_SSO_SECRET
    redis_url: str | None = None
    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_user: str | None = None
    smtp_pass: str | None = None
    smtp_from: str | None = None
    smtp_tls: bool = True
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    marketplace_payment_webhook_secret: str | None = None
    marketplace_payment_token_secret: str | None = None

    esf_base_url: str = "https://esf.gov.kz:8443/esf-web/rest/api"
    esf_username: str | None = None
    esf_password: str | None = None
    esf_seller_bin: str | None = None

    model_config = SettingsConfigDict(env_prefix="SKLAD_", env_file=".env")

    def database_url_matches_backend(self) -> bool:
        if self.database_backend == "sqlite":
            return self.database_url.startswith("sqlite:///")
        return self.database_url.startswith(("postgresql://", "postgresql+psycopg://"))

    def database_backend_allowed_for_mode(self) -> bool:
        return self.deployment_mode == "demo" or self.database_backend == "postgresql"

    def runtime_configuration_error(self) -> str | None:
        if not self.database_url_matches_backend():
            return "SKLAD_DATABASE_BACKEND does not match SKLAD_DATABASE_URL"
        if not self.database_backend_allowed_for_mode():
            return "SQLite is allowed only in SKLAD_DEPLOYMENT_MODE=demo"
        if self.deployment_mode == "production":
            if self.public_access_enabled and not self.production_public_access_acknowledged:
                return (
                    "Production public access requires "
                    "SKLAD_PRODUCTION_PUBLIC_ACCESS_ACKNOWLEDGED=true"
                )
            if self.dev_auth_enabled:
                return "SKLAD_DEV_AUTH_ENABLED must be false in production"
            if not self.oidc_enabled and not self.jwt_hmac_secret:
                return "Production requires SKLAD_JWT_HMAC_SECRET or SKLAD_OIDC_ENABLED=true"
        return None

    @property
    def sqlite_path(self) -> str:
        if self.database_backend != "sqlite":
            raise ValueError("SQLite path is only available for sqlite:/// database URLs")
        if not self.database_url_matches_backend():
            raise ValueError("SQLite backend requires sqlite:/// database URL")
        return self.database_url.removeprefix("sqlite:///")


@lru_cache
def get_settings() -> Settings:
    return Settings()
