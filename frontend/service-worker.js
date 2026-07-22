// Sklad PWA Service Worker — v2
// App shell caching + offline mutation queue via IndexedDB

// Bump CACHE_NAME whenever app.js version changes — forces fresh SW install for all users
const CACHE_NAME = "sklad-pwa-shell-v106";
const DB_NAME = "sklad-offline-queue";
const DB_VERSION = 1;
const QUEUE_STORE = "mutations";

const APP_SCOPE = new URL(self.registration.scope).pathname;
// Versioned app.js so the SW cache is always in sync with what the HTML requests
const APP_SHELL = [
  APP_SCOPE,
  `${APP_SCOPE}app.js?v=97`,
  `${APP_SCOPE}styles.css`,
  `${APP_SCOPE}manifest.webmanifest`,
  `${APP_SCOPE}html5-qrcode.min.js`,
];

// Paths of mutating API endpoints that should be queued offline
const QUEUEABLE_PATHS = [
  "/api/v1/write-offs",
  "/sklad/api/v1/write-offs",
  "/api/v1/write-offs/fefo",
  "/sklad/api/v1/write-offs/fefo",
  "/api/v1/transfers",
  "/sklad/api/v1/transfers",
  "/api/v1/receipts",
  "/sklad/api/v1/receipts",
  "/api/v1/returns/from-department",
  "/sklad/api/v1/returns/from-department",
];

// ── IndexedDB helpers ─────────────────────────────────────────────────────────

function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(QUEUE_STORE)) {
        const store = db.createObjectStore(QUEUE_STORE, { keyPath: "id", autoIncrement: true });
        store.createIndex("createdAt", "createdAt");
      }
    };
    req.onsuccess = (e) => resolve(e.target.result);
    req.onerror = () => reject(req.error);
  });
}

async function enqueue(entry) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(QUEUE_STORE, "readwrite");
    tx.objectStore(QUEUE_STORE).add(entry);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function dequeueAll() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(QUEUE_STORE, "readonly");
    const req = tx.objectStore(QUEUE_STORE).index("createdAt").getAll();
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function removeFromQueue(id) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(QUEUE_STORE, "readwrite");
    tx.objectStore(QUEUE_STORE).delete(id);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function getQueueCount() {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(QUEUE_STORE, "readonly");
    const req = tx.objectStore(QUEUE_STORE).count();
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

// ── Install ───────────────────────────────────────────────────────────────────

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting()),
  );
});

// ── Activate ──────────────────────────────────────────────────────────────────

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) =>
        Promise.all(
          cacheNames
            .filter((n) => n !== CACHE_NAME)
            .map((n) => caches.delete(n)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});

// ── Fetch ─────────────────────────────────────────────────────────────────────

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  const isAppOrigin = url.origin === self.location.origin;

  if (!isAppOrigin) return;

  // Only handle POST mutations we can queue
  if (event.request.method === "POST" && QUEUEABLE_PATHS.some((p) => url.pathname === p)) {
    event.respondWith(handleMutation(event.request));
    return;
  }

  if (event.request.method !== "GET") return;
  if (!url.pathname.startsWith(APP_SCOPE)) return;

  // Navigate → network first, fallback to cache
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(APP_SCOPE, copy));
          return response;
        })
        .catch(() => caches.match(APP_SCOPE)),
    );
    return;
  }

  // Static assets → network first, update cache, fallback to cache
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        }
        return response;
      })
      .catch(() => caches.match(event.request)),
  );
});

// ── Mutation handler ──────────────────────────────────────────────────────────

async function handleMutation(request) {
  let bodyText = null;
  try {
    bodyText = await request.text();
  } catch (_) {
    bodyText = null;
  }

  // Clone the request to replay later (headers + body)
  const headers = {};
  for (const [k, v] of request.headers.entries()) {
    headers[k] = v;
  }

  try {
    // Try sending the request immediately
    const response = await fetch(request.url, {
      method: request.method,
      headers,
      body: bodyText,
    });
    return response;
  } catch (_) {
    // Offline — queue the mutation
    const entry = {
      url: request.url,
      method: request.method,
      headers,
      body: bodyText,
      createdAt: Date.now(),
    };
    await enqueue(entry);

    // Notify all open clients so the UI can show the badge
    const count = await getQueueCount();
    broadcastQueueCount(count);

    // Return a synthetic 202 Accepted so the app knows it was queued
    return new Response(
      JSON.stringify({
        queued: true,
        message: "Операция сохранена для отправки при восстановлении сети",
        queue_size: count,
      }),
      {
        status: 202,
        headers: { "Content-Type": "application/json", "X-Offline-Queued": "1" },
      },
    );
  }
}

// ── Replay queue on sync / online ─────────────────────────────────────────────

self.addEventListener("sync", (event) => {
  if (event.tag === "sklad-offline-sync") {
    event.waitUntil(replayQueue());
  }
});

// Also try to replay when the service worker gets a message
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "REPLAY_QUEUE") {
    replayQueue().then((result) => {
      event.ports[0]?.postMessage(result);
    });
  }
  if (event.data && event.data.type === "GET_QUEUE_COUNT") {
    getQueueCount().then((count) => {
      event.ports[0]?.postMessage({ count });
      broadcastQueueCount(count);
    });
  }
});

async function replayQueue() {
  const entries = await dequeueAll();
  if (!entries.length) return { replayed: 0, failed: 0 };

  let replayed = 0;
  let failed = 0;

  for (const entry of entries) {
    try {
      const response = await fetch(entry.url, {
        method: entry.method,
        headers: entry.headers,
        body: entry.body,
      });
      if (response.ok || response.status === 201 || response.status === 202) {
        await removeFromQueue(entry.id);
        replayed++;
      } else {
        // Non-network error (e.g. validation) — remove from queue to avoid infinite replay
        await removeFromQueue(entry.id);
        failed++;
      }
    } catch (_) {
      // Still offline — keep in queue
      failed++;
    }
  }

  const remaining = await getQueueCount();
  broadcastQueueCount(remaining);

  if (replayed > 0) {
    broadcastEvent("SYNC_COMPLETE", { replayed, failed, remaining });
  }

  return { replayed, failed, remaining };
}

function broadcastQueueCount(count) {
  self.clients.matchAll({ includeUncontrolled: true, type: "window" }).then((clients) => {
    clients.forEach((client) =>
      client.postMessage({ type: "QUEUE_COUNT_UPDATE", count }),
    );
  });
}

function broadcastEvent(type, payload) {
  self.clients.matchAll({ includeUncontrolled: true, type: "window" }).then((clients) => {
    clients.forEach((client) => client.postMessage({ type, ...payload }));
  });
}
