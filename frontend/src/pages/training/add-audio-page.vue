<!-- frontend/src/pages/training/add-audio-page.vue -->

<template>
  <div >
    <!-- Normal Machine Sound -->
    <div>
      <p class="mb-3">Normal Machine Sound</p>
      <div class="row mb-4">
        <div class="coolinput col-6">
              <label class="text">Normal Audio Title*</label>
              <input type="text" placeholder="Add Normal Audio Title..." class="input" required v-model="normalAudioTitle" />
            </div>
        <div class="coolinput col-6" style="position: relative;">
          <label for="fileInput" class="text">Upload Normal Sound*</label>
          <input type="text" :placeholder="normalSoundFile?.name || 'Upload Normal Machine Sound...'" readonly class="upload-input input" disabled />
          <button type="button" class="upload-btn" @click="triggerFileUpload" :disabled="isUploading">
            {{ isUploading ? 'Uploading...' : 'Upload' }}
          </button>
          <input ref="hiddenFileInput" type="file" accept=".mp3,.wav" @change="handleFileUpload" style="display: none;" required />
        </div>
      </div>
      <hr />
    </div>

    <!-- Known faulty Machine Sound -->
    <div>
      <div class="d-flex justify-content-between align-items-center mb-3">
        <p>Known Faulty Machine Sound</p>
        <button type="button" class="add-btn" @click="addKnownFault" :title="isKnownFaultSectionActive ? 'Add another fault' : 'Add known fault'">+</button>
      </div>

      <div v-if="!isKnownFaultSectionActive" class="mb-4">
        <p style="color: var(--accent-color3); font-style: italic; text-align: center; padding: 20px;">Click the + button above to add known faulty machine sounds (optional)</p>
      </div>

      <div v-if="isKnownFaultSectionActive">
        <div v-for="(fault, index) in knownFaults" :key="fault.id" class="mb-4">
          <div class="row mb-4">
            <div class="coolinput col-6">
              <label class="text">Fault Title*</label>
              <input type="text" placeholder="Add Fault Title..." v-model="fault.name" class="input" required />
            </div>

            <div class="coolinput col-6" style="position: relative;">
              <label class="text">Fault Audio*</label>
              <input type="text" :placeholder="fault.file?.name || 'Upload Fault Sound...'" readonly class="upload-input input" style="padding-right: 80px;" />
              <button type="button" class="upload-btn" @click="triggerFaultFileUpload(index)" :disabled="fault.uploading">
                {{ fault.uploading ? 'Uploading...' : 'Upload' }}
              </button>
              <input type="file" accept=".mp3,.wav" :ref="el => setFaultFileRef(el, index)" @change="(e) => handleFaultFileUpload(e, index)" style="display: none;" required />
            </div>
          </div>

          <div class="row mb-3">
            <div class="coolinput col-11">
              <label class="text">Fault Description</label>
              <textarea placeholder="Write here..." v-model="fault.description" class="input"></textarea>
            </div>

            <div class="col-1 d-flex align-items-end" v-if="knownFaults.length >= 1">
              <button type="button" @click="removeKnownFault(index)" title="Remove this fault" style="width: 40px; height: 40px; border-radius: 50%; background-color: transparent; border: none; font-size: 18px; cursor: pointer;">
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
      <div class="row mb-4">
        <div class="d-flex justify-content-end gap-2 mt-4">
          <button type="button" class="button button-primary" @click="submitForm" :disabled="isSubmitting">
            {{ isSubmitting ? 'Submitting...' : 'Next' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const route = useRoute()
const machineId = route.params.machineId
const machine = ref(null)
const isSubmitting = ref(false);
const router = useRouter()

const normalSoundFile = ref(null)
const hiddenFileInput = ref(null)
const isUploading = ref(false)

const knownFaults = ref([])
const isKnownFaultSectionActive = ref(false)
const faultFileInputs = ref([])
const emit = defineEmits(['upload-complete'])
const normalAudioTitle = ref('');


onMounted(async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/machines/${machineId}`)
    if (!response.ok) throw new Error('Machine not found')
    machine.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch machine:', error)
  }
})

function triggerFileUpload() {
  hiddenFileInput.value?.click()
}

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  normalSoundFile.value = file
}

function addKnownFault() {
  knownFaults.value.push({
    id: Date.now(),
    name: '',
    description: '',
    file: null,
    uploading: false
  })
  isKnownFaultSectionActive.value = true
}

function removeKnownFault(index) {
  knownFaults.value.splice(index, 1)
  if (knownFaults.value.length === 0) isKnownFaultSectionActive.value = false
}

function setFaultFileRef(el, index) {
  faultFileInputs.value[index] = el
}

function triggerFaultFileUpload(index) {
  faultFileInputs.value[index]?.click()
}

function handleFaultFileUpload(event, index) {
  const file = event.target.files[0]
  if (!file) return
  knownFaults.value[index].file = file
}

async function submitForm() {
  if (!normalSoundFile.value) {
    alert("Please upload a normal sound file.");
    return;
  }
  isSubmitting.value = true;

  try {
    const formData = new FormData();
    formData.append('file', normalSoundFile.value);
    formData.append('title', normalAudioTitle.value);
    formData.append('type', 'normal');
    formData.append('machine_id', machineId);
    formData.append('user_id', machine.value.user_id);
    formData.append('description', '');

    const normalRes = await fetch(`${API_BASE_URL}/normal_audio_samples`, {
      method: 'POST',
      body: formData
    });

    if (!normalRes.ok) throw new Error('Normal sound upload failed')

    for (const fault of knownFaults.value) {
      if (!fault.name || !fault.file) continue

      const faultFormData = new FormData();
      faultFormData.append('file', fault.file);
      faultFormData.append('machine_id', machineId);
      faultFormData.append('name', fault.name);
      faultFormData.append('description', fault.description);

      const faultRes = await fetch(`${API_BASE_URL}/faults`, {
        method: 'POST',
        body: faultFormData
      });

      if (!faultRes.ok) {
        console.error(`Fault upload failed for ${fault.name}`);
      }
    }

    alert('All audio files uploaded successfully!');
    emit('upload-complete')

  } catch (err) {
    console.error(err);
    alert(`Submit failed: ${err.message}`);
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<style scoped>
.add-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: transparent;
  color: var(--accent-color1);
  border: 2px solid var(--accent-color1);
  font-size: 32px;
  cursor: pointer;
}
.add-btn:disabled,
.upload-btn:disabled,
.button-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.upload-btn {
  position: absolute;
  right: 28px;
  top: 64%;
  transform: translateY(-50%);
  background-color: var(--accent-color1);
  border: none;
  color: var(--ui-1);
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.upload-input {
  padding: 20px 10px;
}
</style>