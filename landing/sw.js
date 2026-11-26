const CACHE = "fito-landing-v1";
const APP_SHELL = ["/", "/static/landing/styles.css", "/static/landing/app.js", "/static/landing/icon.svg", "/static/landing/icon-maskable.svg", "/manifest.webmanifest"];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});
self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  if (req.mode === "navigate") {
    event.respondWith(fetch(req).catch(() => caches.match("/")));
    return;
  }
  if (new URL(req.url).pathname.startsWith("/static/landing/")) {
    event.respondWith(caches.match(req).then(cached => cached || fetch(req)));
  }
});
