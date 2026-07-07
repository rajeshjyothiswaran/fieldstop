/* Fieldstop — offline service worker */
/* VERSION is kept in parity with the <meta name="fieldstop-version"> in fieldstop.html by deploy.sh */
var VERSION = '1.2.0';
var CACHE = 'fieldstop-v' + VERSION;
var ASSETS = [
  './','./index.html','./fieldstop.html',
  './assets/app.css','./assets/app.js',
  './assets/systems/gfx100s.js',
  './assets/systems/gfx100sii.js',
  './fieldstop.webmanifest',
  './icons/icon.svg','./icons/icon-192.png','./icons/icon-512.png','./icons/icon-180.png','./icons/icon-maskable-512.png'
  /* add more camera modules here, e.g. './assets/systems/xt5.js' */
];
self.addEventListener('install', function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){ return c.addAll(ASSETS); }).then(function(){ return self.skipWaiting(); }));
});
self.addEventListener('activate', function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.map(function(k){ if(k!==CACHE) return caches.delete(k); }));
  }).then(function(){ return self.clients.claim(); }));
});
self.addEventListener('fetch', function(e){
  if(e.request.method!=='GET') return;
  e.respondWith(caches.match(e.request).then(function(hit){
    if(hit) return hit;
    return fetch(e.request).then(function(res){
      var copy=res.clone(); caches.open(CACHE).then(function(c){ c.put(e.request,copy); }).catch(function(){});
      return res;
    }).catch(function(){ return caches.match('./fieldstop.html'); });
  }));
});
