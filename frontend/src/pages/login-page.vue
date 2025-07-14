<template>
  <div class="signin-wrapper">
    <div class="signin-card">
      <span class="hero-heading mb-3">Log in</span>
      <div class="w-100">
        <div class="d-flex flex-column mb-4">
          <div class="coolinput mb-4">
            <label class="text">Email</label>
            <input v-model="email" type="email" placeholder="Enter your email" class="input" />
          </div>
          <div class="coolinput mb-4">
            <label class="text">Password</label>
            <input v-model="passwordHash" type="password" placeholder="Enter your password" class="input" />
          </div>
          <button @click="login" class="button button-solid mt-3">Sign in</button>
          <span class="link-text">
            Don’t have an account? <RouterLink to="/register" class="link-pass">Register</RouterLink>
          </span>
          <p v-if="errorMessage" class="error mt-2">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { loginUser } from '../services/userService';

const email = ref('');
const passwordHash = ref('');
const errorMessage = ref('');
const router = useRouter();
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const login = async () => {
  try {
    const response = await loginUser(email.value, passwordHash.value);
    localStorage.setItem('token', response.access_token);
    router.push('/');
  } catch (err) {
    errorMessage.value = err?.response?.data?.detail || 'Login failed';
    console.error(err);
  }
};
</script>
