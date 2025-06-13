self.addEventListener("install", event => {
  console.log("Vaudreuil Forum service worker installed.");
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  console.log("Vaudreuil Forum service worker activated.");
});

self.addEventListener("fetch", event => {
  // Basic pass-through (can be extended for caching)
  event.respondWith(fetch(event.request));
});
