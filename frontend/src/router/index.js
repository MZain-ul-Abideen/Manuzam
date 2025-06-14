// frontend/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/dashboard-page.vue'
import Diagnosis from '../pages/diagnosis-page.vue'
import ListMachine from '../pages/list-machine-page.vue'
import AddMachine from '../pages/add-machine-page.vue'
import UserProfile from '../pages/profile-page.vue'
import NotFound from '../pages/404-page.vue'
import LogIn from '../pages/login-page.vue'
import Register from '../pages/register-page.vue'
import ListUser from '../pages/list-user-page.vue'

// Define routes
const routes = [
  { path: '/', redirect: '/dashboard' },

  // 🔒 Protected Routes (require login)
  { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: false } },
  { path: '/diagnosis', name: 'Diagnosis', component: Diagnosis, meta: { requiresAuth: false } },
  { path: '/list_machines', name: 'ListMachine', component: ListMachine, meta: { requiresAuth: false } },
  { path: '/AddMachine', name: 'AddMachine', component: AddMachine, meta: { requiresAuth: false } },
  { path: '/profile', name: 'UserProfile', component: UserProfile, meta: { requiresAuth: false } },
  { path: '/list_users', name: 'ListUser', component: ListUser, meta: { requiresAuth: false } },

  // Public routes
  { path: '/login', name: 'LogIn', component: LogIn },
  { path: '/register', name: 'Register', component: Register },

  // 404 catch-all
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
]

// Create the router
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ⛔️ Route Guard: redirect to /login if not authenticated
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/dashboard') // already logged in, don't allow going back to login/register
  } else {
    next()
  }
})

export default router
