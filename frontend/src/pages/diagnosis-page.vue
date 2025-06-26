<script setup>
import { ref } from 'vue'
import Banner from '../components/banner-component.vue'

const selectedFile = ref(null)
const uploadStatus = ref('')
const fileInput = ref(null)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function triggerFileInput() {
  fileInput.value?.click()
}

async function handleAndUpload(event) {
  selectedFile.value = event.target.files[0]
  uploadStatus.value = ''

  if (!selectedFile.value) {
    alert('No file selected.')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`)
    }

    const result = await response.json()
    console.log('Upload successful:', result)
    uploadStatus.value = 'File uploaded successfully!'
  } catch (error) {
    console.error('Upload failed:', error)
    uploadStatus.value = 'Upload failed. Please try again'
  }
}
</script>


<template>
  <div>
    <Banner />
  </div>
  <div class="wrapper">
    <h1 class="mb-4 mt-3">Click to Record</h1>

    <div class="record-button-ring">
      <button class="record-button"><img src="../assets/icons/record.svg" /></button>
    </div>

    <!-- Hidden file input -->
    <input
      type="file"
      accept="audio/*"
      ref="fileInput"
      @change="handleAndUpload"
      style="display: none"
    />

    <!-- Upload button -->
    <button class="button button-primary mt-4" @click="triggerFileInput">
      <img src="../assets/icons/upload.svg" class="upload-icon" />Upload
    </button>

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
  padding-right: 0.5rem;
}
</style>
