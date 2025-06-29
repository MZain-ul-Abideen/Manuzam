<template>
  <div class="signin-wrapper">
    <div class="signin-card">
      <span class="hero-heading mb-3">Register</span>
      <div class="w-100">
        <div class="d-flex flex-column mb-4">
          <div class="coolinput mb-4">
            <label class="text">Name</label>
            <input v-model="name" type="text" placeholder="Enter your name" class="input" />
          </div>
          <div class="coolinput mb-4">
            <label class="text">Email</label>
            <input v-model="email" type="email" placeholder="Enter your email" class="input" />
          </div>
          <div class="coolinput mb-4">
            <label class="text">Password</label>
            <input v-model="passwordHash" type="password" placeholder="Enter your password" class="input" />
          </div>
          <button @click="register" class="button button-solid mt-3">Register</button>
          <span class="link-text">
            Already have an account? <RouterLink to="/login" class="link-pass">Sign in</RouterLink>
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
import { createUser } from '../services/userService';

const name = ref('');
const email = ref('');
const passwordHash = ref('');
const errorMessage = ref('');
const router = useRouter();
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const register = async () => {
  try {
    await createUser({
      username: name.value,
      email: email.value,
      password_hash: passwordHash.value,
    });
    router.push('/');
  } catch (err) {
    errorMessage.value = err?.response?.data?.detail || 'Registration failed.';
    console.error(err);
  }
};
</script>
