<!-- frontend/src/pages/training-page.vue -->
<template>
  <div>
    <Banner v-if="machine" :machineName="machine.name" />
  </div>

  <div v-if="loading" class="text-center mt-5">
    Loading machine details...
  </div>

  <div v-else class="card-container">
    <ul class="ProgressSteps">
      <li v-for="(stepItem, index) in steps" :key="index" :class="[
        'step',
        { active: step === index + 1, completed: isStepCompleted(index + 1) }
      ]" @click="goToStep(index + 1)">
        <span class="step-number" :class="{
          'step-accent': step === index + 1 || isStepCompleted(index + 1)
        }">
          {{ index + 1 }}
        </span>
        <span class="step-label">{{ stepItem }}</span>
      </li>

    </ul>


    <!-- Step 1: Audio Upload -->
    <div v-if="step === 1">
      <AudioUploadStep :machine="machine" @upload-complete="onAudioUploadComplete" />
    </div>

    <!-- Step 2: Sensor Configuration -->
    <div v-if="step === 2">
      <SensorConfigStep :machine-id="machineId" @upload-complete="onSensorSubmitComplete" />
    </div>

    <!-- Step 3: Feature Extraction -->
    <div v-if="step === 3">
      <FeaturesExtrationStep :machine-id="machineId" @upload-complete="onFeatureExtrationComplete" />
    </div>


  </div>
</template>

<script setup>
import Banner from '../components/banner-component.vue'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AudioUploadStep from '../pages/training/add-audio-page.vue'
import SensorConfigStep from '../pages/training/add-sensors-page.vue'
import FeaturesExtrationStep from '../pages/training/extract-features-page.vue'

const route = useRoute()
const router = useRouter()
const machineId = route.params.machineId

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const machine = ref(null)
const step = ref(1)
const audioUploaded = ref(false)
const loading = ref(true)

const steps = ['Audio Details', 'Sensor Details', 'Feature Extraction']
const featureExtracted = ref(false)

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/machines/${machineId}`)
    if (!res.ok) throw new Error('Machine not found')
    machine.value = await res.json()
  } catch (err) {
    console.error('Failed to load machine:', err)
  } finally {
    loading.value = false
  }
})

function isStepCompleted(stepNumber) {
  if (stepNumber === 1) return true
  if (stepNumber === 2) return audioUploaded.value
  if (stepNumber === 3) return featureExtracted.value
  return false
}


function goToStep(targetStep) {
  if (targetStep < step.value || isStepCompleted(targetStep)) {
    step.value = targetStep
  }
}

function onAudioUploadComplete() {
  audioUploaded.value = true
  step.value = 2
}

function onSensorSubmitComplete() {
  step.value = 3
}

function onFeatureExtrationComplete() {
  featureExtracted.value = true
  router.push({ name: 'ListMachine' })
}
</script>


<style scoped>
.ProgressSteps {
  display: flex;
  justify-content: space-between;
  list-style: none;
  padding: 0;
  margin: 20px 0;
}

.step {
  flex: 1;
  text-align: center;
  position: relative;
  cursor: default;
  transition: 0.3s;
}

.step.completed,
.step.active {
  cursor: pointer;
  opacity: 1;
  font-weight: bold;
}

.step-number {
  display: inline-block;
  color: var(--accent-color1);
  border-radius: 50%;
  width: 30px;
  height: 30px;
  line-height: 30px;
  font-size: 14px;
  margin-bottom: 5px;
  background: var(--primary-1);
  border: 1px var(--accent-color3) solid;
}

.step-number.step-accent {
  background: var(--accent-color1);
  color: var(--ui-3);
}

.step-label {
  display: block;
  font-size: 14px;
}

/* Connector lines BEFORE each step */
.step:not(:first-child)::before {
  content: "";
  position: absolute;
  top: 15px;
  left: -50%;
  width: 100%;
  height: 2px;
  background: var(--ui-2); /* default connector color */
  z-index: -1;
}

/* Connector highlighted if current step is active/completed OR if previous step is completed */
.step.completed:not(:first-child)::before,
.step.active:not(:first-child)::before {
  background: var(--accent-color1);
}
</style>