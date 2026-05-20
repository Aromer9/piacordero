import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '../composables/useAuth.js'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/admin/productos',
      },
      {
        path: 'productos',
        name: 'admin-products',
        component: () => import('../views/admin/AdminProducts.vue'),
      },
      {
        path: 'contenido',
        name: 'admin-content',
        component: () => import('../views/admin/AdminContent.vue'),
      },
      {
        path: 'analytics',
        name: 'admin-analytics',
        component: () => import('../views/admin/AdminAnalytics.vue'),
      },
    ],
  },
  {
    path: '/admin/login',
    name: 'admin-login',
    component: () => import('../views/admin/AdminLogin.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth', top: 68 }
    }
    if (savedPosition) return savedPosition
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !getToken()) {
    return { name: 'admin-login', query: { redirect: to.fullPath } }
  }
})

export default router
