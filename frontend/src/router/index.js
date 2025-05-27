// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Diagnosis from '../pages/diagnosis-page.vue'
import Dashboard from '../pages/dashboard-page.vue'

const routes = [
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/diagnosis', name: 'Diagnosis', component: Diagnosis },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
