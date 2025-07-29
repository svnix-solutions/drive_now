import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/pages/Dashboard.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
  },
  {
    path: '/book-ride',
    name: 'BookRide',
    component: () => import('@/pages/BookRide.vue'),
  },
  {
    path: '/ride-history',
    name: 'RideHistory',
    component: () => import('@/pages/RideHistory.vue'),
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/pages/Profile.vue'),
  },
  {
    path: '/ride-tracking/:rideId',
    name: 'RideTracking',
    component: () => import('@/pages/RideTracking.vue'),
    props: true,
  },
]

let router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

export default router
