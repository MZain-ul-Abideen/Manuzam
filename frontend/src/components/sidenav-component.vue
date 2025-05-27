<template>
    <div class="d-flex flex-column vh-100 bg-dark text-white p-3" style="width: 250px;">
      <!-- Logo -->
      <div class="mb-4">
        <h2 class="text-accent">MyLogo</h2>
      </div>
  
      <!-- Navigation Links -->
      <nav class="flex-grow-1">
        <ul class="nav flex-column">
          <li class="nav-item mb-3" v-for="(link, index) in navLinks" :key="index">
            <a class="nav-link text-white" href="#">{{ link }}</a>
          </li>
        </ul>
      </nav>
  
      <!-- Logout Button -->
      <div>
        <button class="btn btn-outline-light w-100">Logout</button>
      </div>
    </div>
  </template>
  
  <script setup>
  const navLinks = ['Dashboard', 'Reports', 'Analytics', 'Settings', 'Profile']
  </script>
  
  <style scoped>
  .bg-dark {
    background-color: var(--ui-2) !important;
  }
  
  .text-accent {
    color: var(--accent-color1);
    font-size: var(--h1);
    font-family: var(--font-main);
  }
  </style>
  