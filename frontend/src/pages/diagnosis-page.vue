<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Banner from '../components/banner-component.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const router = useRouter()

const machineId = route.params.machineId

// Data refs
const machine = ref(null)
const sensor = ref(null)

const selectedFile = ref(null)
const fileInput = ref(null)

const temperature = ref(null)
const vibration = ref(null)

const isSubmitting = ref(false)
const uploadStatus = ref('')
const loading = ref(true)  // Loading state

// Fetch machine & sensor data
onMounted(async () => {
  try {
    const machineRes = await fetch(`${API_BASE_URL}/machines/${machineId}`)
    if (!machineRes.ok) {
      router.replace({ name: 'NotFound' })
      return
    }
    machine.value = await machineRes.json()

    const sensorRes = await fetch(`${API_BASE_URL}/sensors/machine/${machineId}`)
    sensor.value = sensorRes.ok ? await sensorRes.json() : null
  } catch (error) {
    console.error('Error loading machine or sensor:', error)
    router.replace({ name: 'NotFound' })
  } finally {
    loading.value = false
  }
})

// UI logic
const showTempField = computed(() =>
  selectedFile.value && sensor.value?.temperature_sensor_enabled
)

const showVibField = computed(() =>
  selectedFile.value && sensor.value?.vibration_sensor_enabled
)

const diagnoseEnabled = computed(() => {
  if (!selectedFile.value) return false
  if (showTempField.value && (temperature.value === null || temperature.value === '')) return false
  if (showVibField.value && (vibration.value === null || vibration.value === '')) return false
  return true
})

// Event handlers
function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(event) {
  selectedFile.value = event.target.files[0] || null
  uploadStatus.value = ''
}

// Final submit
async function handleFinalSubmit() {
  if (!diagnoseEnabled.value) return

  isSubmitting.value = true
  uploadStatus.value = ''

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('machine_id', machineId)
    formData.append('temperature_value', showTempField.value ? temperature.value : null)
    formData.append('vibration_value', showVibField.value ? vibration.value : null)

    const response = await fetch(`${API_BASE_URL}/diagnose`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) throw new Error('Diagnosis failed')

    const result = await response.json()
    console.log('Diagnosis success:', result)
    uploadStatus.value = 'Diagnosis successful!'
  } catch (error) {
    console.error('Submission failed:', error)
    uploadStatus.value = `Error: ${error.message}`
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div>
    <Banner :machineName="machine?.name" />
  </div>

  <div v-if="loading" class="text-center mt-5">
    Loading machine details...
  </div>

  <div v-else class="wrapper">
    <h1 class="mb-4 mt-3">Diagnose Machine</h1>

    <!-- File input (hidden) -->
    <input
      type="file"
      accept="audio/*"
      ref="fileInput"
      @change="handleFileSelect"
      style="display: none"
    />

    <div class="record-button-ring">
      <button class="record-button" @click="triggerFileInput">
        <img src="../assets/icons/record.svg" />
      </button>
    </div>

    <div class="mt-3 d-flex">

    <!-- Temperature Field -->
    <div v-if="showTempField" class="coolinput mx-1">
      <input
        v-model="temperature"
        type="number"
        placeholder="Enter temperature"
        class="input"
      />
    </div>

    <!-- Vibration Field -->
    <div v-if="showVibField" class="coolinput mx-1">
      <input
        v-model="vibration"
        type="number"
        placeholder="Enter vibration"
        class="input"
      />
    </div>
    </div>

    <!-- Diagnose Button -->
    <button
      class="button button-primary mt-4"
      :disabled="!diagnoseEnabled || isSubmitting"
      @click="handleFinalSubmit"
    >
      <svg
        class="upload-icon"
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        fill="currentColor"
        viewBox="0 0 24 24"
      >
        <path d="M5 20h14v-2H5v2zm7-14l-5 5h3v4h4v-4h3l-5-5z" />
      </svg>
      {{ isSubmitting ? 'Diagnosing...' : 'Diagnose' }}
    </button>

    <div v-if="selectedFile" class="mt-3">
      Selected File: {{ selectedFile.name }}
    </div>

    <div v-if="uploadStatus" class="mt-2">{{ uploadStatus }}</div>
  </div>
</template>

<style scoped>
.wrapper {
  max-width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.record-button-ring {
  background-color: transparent;
  padding: 0.7rem;
  border-radius: 50%;
  border: 4px solid var(--accent-color1);
}

.record-button {
  background: var(--accent-color2);
  border: none;
  cursor: pointer;
  height: 25rem;
  width: 25rem;
  border-radius: 50%;
}

.upload-icon {
  fill: var(--accent-color1) !important;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border: 1px solid var(--accent-color3) !important;
  color: var(--accent-color3) !important;
  fill: var(--accent-color3) !important;
}
button:disabled:hover {
  box-shadow: none;
}

button:disabled .upload-icon {
  fill: var(--accent-color3) !important;
}

</style>
