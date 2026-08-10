from django.http import HttpResponse, JsonResponse, Http404

from .models import PWASettings


def pwa_manifest(request):
    """
    Dynamic web app manifest, built from the admin-configured PWASettings row.
    Returns 404 when PWA install is disabled so browsers won't treat the
    site as installable.
    """
    settings_obj = PWASettings.objects.first()
    if not settings_obj or not settings_obj.is_enabled:
        raise Http404

    icon_url = settings_obj.icon_url
    icons = []
    if icon_url:
        icons = [
            {'src': icon_url, 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any maskable'},
            {'src': icon_url, 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'},
        ]

    manifest = {
        'name':             settings_obj.app_name,
        'short_name':       settings_obj.app_name,
        'start_url':        '/',
        'scope':             '/',
        'display':          'standalone',
        'background_color': '#ffffff',
        'theme_color':      '#1a3a8f',
        'icons':            icons,
    }
    return JsonResponse(manifest, content_type='application/manifest+json')


_SERVICE_WORKER_JS = """
// BoosterNotes service worker — caches static assets for fast repeat loads.
// Registered only when PWA install is enabled (see index.html).
const CACHE_NAME = 'boosternotes-static-v1';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n)))
    )
  );
  self.clients.claim();
});

// Cache-first for hashed static assets (CSS/JS/fonts) — they never change
// content under the same URL, so this is always safe.
// Everything else (HTML, API calls, Dropbox media) goes straight to the
// network — those change too often / are access-controlled to cache blindly.
self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin === self.location.origin && url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.open(CACHE_NAME).then((cache) =>
        cache.match(req).then((cached) => {
          if (cached) return cached;
          return fetch(req).then((res) => {
            if (res.ok) cache.put(req, res.clone());
            return res;
          });
        })
      )
    );
  }
});
"""


def pwa_service_worker(request):
    """
    Serves the service worker at the site root so its default scope covers
    the whole site (a scope no static-file host under /static/ could grant
    without extra headers). Content is static; PWA-enabled gating happens
    client-side in index.html, which only registers this when enabled.
    """
    response = HttpResponse(_SERVICE_WORKER_JS, content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache'
    return response
