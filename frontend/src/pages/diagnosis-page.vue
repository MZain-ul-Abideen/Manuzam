<!-- frontend/src/pages/diagnosis-page.vue -->

<template>
  <div>
    <Banner :machine-name="machine?.name || ''" />
  </div>

  <LandingPage v-if="!machineId" />
  <DashboardPage
    v-else
    :machine-id="machineId"
    :machine="machine"
    :loading="loading"
  />
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import Banner from '@/components/banner-component.vue'
import LandingPage from '../pages/diagnosis/landing-page.vue'
import DashboardPage from '../pages/diagnosis/dashboard-page.vue'

const route = useRoute()
const machineId = route.params.machineId

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const machine = ref(null)
const loading = ref(true)

onMounted(() => {
  if (machineId) {
    fetchMachine()
  } else {
    loading.value = false
  }
})

async function fetchMachine() {
  try {
    const res = await fetch(`${API_BASE_URL}/machines/${machineId}`)
    if (!res.ok) throw new Error('Machine not found')
    machine.value = await res.json()
  } catch (err) {
    console.error('Failed to load machine:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Optional styling */
</style>
