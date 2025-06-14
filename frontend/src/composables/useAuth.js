// src/composables/useAuth.js
import { ref } from 'vue'
import api from '../api'

const user = ref(null)

export async function fetchCurrentUser() {
  try {
    const res = await api.get('/auth/me')
    user.value = res.data
  } catch (err) {
    user.value = null
    localStorage.removeItem('token')
  }
}

export function getUser() {
  return user
}
