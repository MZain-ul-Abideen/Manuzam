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
 width: 100%;
 height: 100%;
 display: flex;
  justify-content: center;
  align-items: center;
}

.loader::before {
 content: "";
 box-sizing: border-box;
 position: absolute;
 width: 200px;
 height: 200px;
 border-radius: 50%;
 border-top: 10px solid var(--primary-1);
 border-right: 10px solid transparent;
 animation: spinner8217 0.8s linear infinite;
}

@keyframes spinner8217 {
 to {
  transform: rotate(360deg);
 }
}

.text-container {
  background: transparent;
  height: 100px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.text-container h1 {
  position: absolute;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>