<template>
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div>
      <p>{{ currentText?.subheading }}</p>
      <h1>{{ currentText?.headind }}</h1>
    </div>
    <router-link to="/profile" class="profile-icon">
      <img src="../assets/profile.svg" alt="Profile" height="100%" width="100%" />
    </router-link>
  </div>
</template>


<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const BannerText = [
  { path: '/dashboard', headind: 'Dashboard', subheading: 'Machine Name Stats' },
  { path: '/diagnosis', headind: 'Diagnosis', subheading: 'Machine Name' },
  { path: '/list_machines', headind: 'All Machines', subheading: 'Updated List' },
  { path: '/list_users', headind: 'All Users', subheading: 'Updated List' },
  { path: '/AddMachine', headind: 'Machine Details', subheading: 'Add Machine Details' },
  { path: '/add-sensors', headind: 'Sensors Details', subheading: 'Add Sensors Details' },
  { path: '/add-audio', headind: 'Audio Details', subheading: 'Add Audio Files' },
  { path: '/profile', headind: 'Profile', subheading: 'Username' },
]

// Compute the banner text based on the current route
const currentText = computed(() => {
  return BannerText.find(text => route.path.startsWith(text.path))
})
</script>

<style scoped>
.profile-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: transparent;
  display: inline-block;
}
</style>