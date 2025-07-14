<!-- frontend/src/pages/training/extract-features-page.vue -->
<script setup>
import { ref } from 'vue'
import trainIcon from '../../assets/icons/train_icon.svg'

const props = defineProps({
  machineId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['upload-complete'])

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const isTraining = ref(false)
const errorMessage = ref("")
const successMessage = ref("")

async function trainMachine() {
  isTraining.value = true
  errorMessage.value = ""
  successMessage.value = ""

  try {
    const response = await fetch(`${API_BASE_URL}/ml_models/train/${props.machineId}`, {
      method: 'POST',
    })

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || 'Training failed')
    }

    const data = await response.json()
    successMessage.value = "Model trained successfully!"

    // Show message for 2s then emit completion
    setTimeout(() => emit('upload-complete'), 2000)

  } catch (err) {
    errorMessage.value = "Error occurred, try again!"
  } finally {
    isTraining.value = false
  }
}
</script>

<template>
  <div class="container d-flex flex-column align-items-center mt-5">
    <div class="wrapper">
      <div class="record-button-ring">
        <button class="record-button" @click="trainMachine" :disabled="isTraining">
          <p v-if="isTraining" class="loader"></p>
          <img :src="trainIcon" alt="Train Icon" v-else />
        </button>
      </div>
      <div class="text-container">
      <transition name="fade">
        <h1 v-if="isTraining" class="text-center mb-4 mt-4">Training in progress...</h1>
      </transition>

      <transition name="fade">
        <h1 v-if="successMessage" class="text-center mb-4 mt-4 success">{{ successMessage }}</h1>
      </transition>

      <transition name="fade">
        <h1 v-if="errorMessage" class="text-center mb-4 mt-4 error text-danger">{{ errorMessage }}</h1>
      </transition>

      <transition name="fade">
        <h1 v-if="!isTraining && !successMessage && !errorMessage" class="text-center mb-4 mt-4">Click to Train Machine</h1>
      </transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loader {
  width: 125px;
  height: 125px;
  margin: auto;
  position: relative;
}

.loader:before {
  content: '';
  width: 120px;
  height: 10px;
  background: #0D5326;
  position: absolute;
  top: 150px;
  left: 0;
  border-radius: 50%;
  animation: shadow324 0.5s linear infinite;
}

.loader:after {
  content: '';
  width: 100%;
  height: 100%;
  background: var(--primary-1);
  position: absolute;
  top: 0;
  left: 0;
  border-radius: 4px;
  animation: jump7456 0.5s linear infinite;
}

@keyframes jump7456 {
  15% {
    border-bottom-right-radius: 3px;
  }

  25% {
    transform: translateY(9px) rotate(22.5deg);
  }

  50% {
    transform: translateY(18px) scale(1, .9) rotate(45deg);
    border-bottom-right-radius: 40px;
  }

  75% {
    transform: translateY(9px) rotate(67.5deg);
  }

  100% {
    transform: translateY(0) rotate(90deg);
  }
}

@keyframes shadow324 {

  0%,
    100% {
    transform: scale(1, 1);
  }

  50% {
    transform: scale(1.2, 1);
  }
}
</style>