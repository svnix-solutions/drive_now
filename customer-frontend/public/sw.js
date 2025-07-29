const CACHE_NAME = 'drive-now-v1';
const urlsToCache = [
  '/',
  '/frontend/',
  '/frontend/index.html',
  '/frontend/assets/index.css',
  '/frontend/assets/index.js',
  '/frontend/assets/vendor.js',
  '/frontend/assets/vendor.css',
  '/frontend/favicon.png',
  '/frontend/icon-192x192.png',
  '/frontend/icon-512x512.png'
];

// Install event - cache resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Parse URL
  const requestURL = new URL(event.request.url);

  // Handle API requests differently (network first)
  if (requestURL.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Clone the response before caching
          const responseToCache = response.clone();
          
          // Cache successful API responses
          if (response.status === 200) {
            caches.open(CACHE_NAME).then(cache => {
              cache.put(event.request, responseToCache);
            });
          }
          
          return response;
        })
        .catch(() => {
          // If network fails, try cache
          return caches.match(event.request);
        })
    );
    return;
  }

  // For other requests, use cache first strategy
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }

        return fetch(event.request).then(response => {
          // Check if valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone the response
          const responseToCache = response.clone();

          // Cache the response
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });

          return response;
        });
      })
      .catch(() => {
        // Offline fallback page
        if (event.request.destination === 'document') {
          return caches.match('/frontend/index.html');
        }
      })
  );
});

// Background sync for ride bookings
self.addEventListener('sync', event => {
  if (event.tag === 'sync-ride-bookings') {
    event.waitUntil(syncRideBookings());
  }
});

async function syncRideBookings() {
  // This will be called when connection is restored
  // Implement logic to sync pending ride bookings
  console.log('Syncing ride bookings...');
}

// Push notifications
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'New notification from Drive Now',
    icon: '/frontend/icon-192x192.png',
    badge: '/frontend/icon-192x192.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'view',
        title: 'View',
        icon: '/frontend/view-icon.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/frontend/close-icon.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Drive Now', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'view') {
    // Open the app when notification is clicked
    event.waitUntil(
      clients.openWindow('/frontend/')
    );
  }
});