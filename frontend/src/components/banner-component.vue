<script setup>
import { computed, defineProps } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  machineName: {
    type: String,
    default: ''
  }
})

const route = useRoute()

const BannerText = [
  { path: '/dashboard', heading: 'Dashboard', subheading: 'Machine Name Stats' },
  { path: '/diagnosis', heading: 'Diagnose', subheading: 'Welcome to Manuzam' },
  { path: '/training', heading: 'Training', subheading: 'Machine Name' },
  { path: '/list_machines', heading: 'All Machines', subheading: 'Updated List' },
  { path: '/list_users', heading: 'All Users', subheading: 'Updated List' },
  { path: '/AddMachine', heading: 'Machine Details', subheading: 'Add Machine Details' },
  { path: '/profile', heading: 'Profile', subheading: 'Username' },
]

const currentText = computed(() => {
  // Special handling for /diagnosis/:id and /diagnosis/:id/result
  if (route.path.startsWith('/diagnosis')) {
    return { heading: 'Diagnose', subheading: 'Welcome to Manuzam' }
  }

  return BannerText.find(text =>
    route.path === text.path || route.path.startsWith(text.path + '/')
  )
})

const subheading = computed(() => {
  // Show machine name if on /diagnosis route (any subpath)
  if (route.path.startsWith('/diagnosis') && props.machineName) {
    return props.machineName
  }
  return currentText.value?.subheading || ''
})

</script>


<template>
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div>
      <p>{{ subheading }}</p>
      <h1>{{ currentText?.heading }}</h1>
    </div>
    <router-link to="/profile" class="profile-icon">
      <img src="../assets/profile.svg" alt="Profile" height="100%" width="100%" />
    </router-link>
  </div>
</template>

<style scoped>
.profile-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: transparent;
  display: inline-block;
}
</style>
