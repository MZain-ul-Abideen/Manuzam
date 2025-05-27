<script setup>
import { ref } from 'vue'

const selectedFile = ref(null)
const uploadStatus = ref('')

function handleFileChange(event) {
  selectedFile.value = event.target.files[0]
  uploadStatus.value = ''
}

async function uploadFile() {
  if (!selectedFile.value) {
    alert('Please select a file to upload.')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const response = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`)
    }

    const result = await response.json()
    console.log('Upload successful:', result)
    uploadStatus.value = '✅ File uploaded successfully!'
  } catch (error) {
    console.error('Upload failed:', error)
    uploadStatus.value = '❌ Upload failed. Please try again.'
  }
}
</script>

<template>
  <div>
    <h1>Diagnosis</h1>
    <hr>

    <input type="file" accept="audio/*" @change="handleFileChange" class="mt-3" />
    <div v-if="selectedFile" class="mt-2">Selected: {{ selectedFile.name }}</div>

    <button class="mt-3" @click="uploadFile">Upload</button>

    <div v-if="uploadStatus" class="mt-2">{{ uploadStatus }}</div>
  </div>
</template>

<style scoped>
.mt-2 {
  margin-top: 0.5rem;
}
.mt-3 {
  margin-top: 1rem;
}
</style>
