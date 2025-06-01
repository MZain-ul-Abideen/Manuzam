import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/dashboard-page.vue'
import Diagnosis from '../pages/diagnosis-page.vue'
import ListMachine from '../pages/list-machine-page.vue'
import AddMachine from '../pages/add-machine-page.vue'
import UserProfile from '../pages/profile-page.vue'
import NotFound from '../pages/404-page.vue'
import LogIn from '../pages/login-page.vue'
import Register from '../pages/register-page.vue'

const routes = [
  { path: '/', redirect: '/dashboard' }, // ✅ Default route

  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/diagnosis', name: 'Diagnosis', component: Diagnosis },
  { path: '/ListMachine', name: 'ListMachine', component: ListMachine },
  { path: '/AddMachine', name: 'AddMachine', component: AddMachine },
  { path: '/profile', name: 'UserProfile', component: UserProfile },
  { path: '/login', name: 'LogIn', component: LogIn },
  { path: '/register', name: 'Register', component: Register },

  // ⚠️ Catch-all route for 404 Not Found
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
