// Offline support for Word Stories on the phone.
// - This site's own files: network first (new stories show up at once), the saved copy when offline.
// - The dictionary's data.js (same origin, /english-words-dictionary/): the copy already on the phone first,
//   from this site's cache or the dictionary's own cache, refreshed in the background.
// - Audio (.mp3) is not handled here: the page reads the dictionary's audio cache itself.
const CACHE = "stories-v1";
const SCOPE = new URL("./", self.location).pathname;   // /word-stories/

self.addEventListener("install", (ev) => {
  ev.waitUntil(caches.open(CACHE).then((c) => c.addAll(["./", "index.html"])).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (ev) => ev.waitUntil(self.clients.claim()));

function save(req, res) {
  if (res && res.ok) {
    const copy = res.clone();
    caches.open(CACHE).then((c) => c.put(req, copy));
  }
  return res;
}

self.addEventListener("fetch", (ev) => {
  const req = ev.request;
  const url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin || url.pathname.endsWith(".mp3")) return;
  if (url.pathname.endsWith("/english-words-dictionary/data.js")) {
    ev.respondWith(caches.match(req, { ignoreSearch: true }).then((hit) => {
      const net = fetch(req).then((res) => save(req, res));
      if (hit) { ev.waitUntil(net.catch(() => {})); return hit; }
      return net;
    }));
    return;
  }
  if (!url.pathname.startsWith(SCOPE)) return;   // other sites on this origin look after themselves
  ev.respondWith(fetch(req).then((res) => save(req, res)).catch(() =>
    caches.match(req, { ignoreSearch: true }).then((hit) => hit || caches.match("index.html"))));
});
