// Service Worker — Dziennik Malucha (PWA)
const CACHE = 'dziennik-malucha-v1';
const SHELL = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-512-maskable.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(SHELL)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  // Tylko własne zasoby cache'ujemy; Firebase/Puter/CDN zawsze z sieci.
  const sameOrigin = url.origin === self.location.origin;

  if (req.mode === 'navigate') {
    // Nawigacja: najpierw sieć, offline -> cache index.html
    event.respondWith(
      fetch(req).catch(() => caches.match('./index.html'))
    );
    return;
  }

  if (sameOrigin) {
    // Statyczne pliki: cache-first, w tle aktualizacja
    event.respondWith(
      caches.match(req).then(cached => {
        const network = fetch(req).then(res => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(req, copy));
          }
          return res;
        }).catch(() => cached);
        return cached || network;
      })
    );
  }
  // Zewnętrzne (Firebase, Puter, Google Fonts itd.) -> domyślnie sieć.
});
