<template>
    <div>
        <Banner />
    </div>
    <div class="card-container">
        <!-- Basic Info -->
        <div>
            <p class="mb-3">Basic Info</p>
            <div class="row mb-4">
                <div class="coolinput col-5">
                    <label for="machineName" class="text">Machine Name*</label>
                    <input type="text" required placeholder="Write Machine Name..." name="machineName" id="machineName" class="input" v-model="formData.machineName">
                </div>
                <div class="coolinput col-5">
                    <label for="manufacturer" class="text">Manufacturer</label>
                    <input type="text" placeholder="Write Manufacturer..." name="manufacturer" id="manufacturer" class="input" v-model="formData.manufacturer">
                </div>
            </div>
            <div class="row mb-5">
                <div class="coolinput col-5">
                    <label for="modelNumber" class="text">Model Number</label>
                    <input type="text" placeholder="Add Model Number..." name="modelNumber" id="modelNumber" class="input" v-model="formData.modelNumber">
                </div>
                <div class="coolinput col-5">
                    <label for="yearOfInstallation" class="text">Year of Installation</label>
                    <select v-model="formData.yearOfInstallation" name="yearOfInstallation" id="yearOfInstallation" class="input select-input"
                        :class="{ 'placeholder-shown': formData.yearOfInstallation === '' }">
                        <option value="" class="option-disabled" disabled>Select year...</option>
                        <option v-for="year in years" :key="year" :value="year" class="select-options">{{ year }}
                        </option>
                    </select>
                </div>
            </div>
            <hr>
        </div>
        <!-- Operational Details -->
        <div>
            <p class="mb-3">Operational Details</p>
            <div class="row mb-4">
                <div class="coolinput col-5">
                    <label for="operatingHours" class="text">Operating Hours per Day*</label>
                    <input type="number" id="operatingHours" name="operatingHours" class="input"
                        placeholder="Enter hours from 1 to 24..." min="1" max="24" v-model.number="formData.operatingHours"
                        @input="checkHours" required>
                </div>

                <div class="coolinput col-5">
                    <label for="maintenanceSchedule" class="text">Maintenance Schedule</label>
                    <input type="number" name="maintenanceSchedule" id="maintenanceSchedule" class="input" min="1" max="365"
                        placeholder="Enter days from 1 to 365..." v-model.number="formData.maintenanceSchedule"
                        @input="checkDays" />
                </div>
            </div>
            <div class="row mb-5">
                <div class="coolinput col-5">
                    <label for="lastMaintenanceDate" class="text">Last Maintenance Date</label>
                    <input type="date" id="lastMaintenanceDate" name="lastMaintenanceDate" :max="today"
                        v-model="formData.lastMaintenanceDate" class="input" :class="{ empty: !formData.lastMaintenanceDate }" />
                </div>
                <div class="coolinput col-5">
                    <label for="expectedLifespan" class="text">Expected Lifespan</label>
                    <input type="number" min="1" placeholder="Enter Years e.g., 10..." name="expectedLifespan"
                        id="expectedLifespan" v-model="formData.expectedLifespan" class="input">
                </div>

            </div>
            <hr>
        </div>
        <!-- Sensor Configuration -->
        <div>
            <p class="mb-3">Sensor Configuration</p>
            <div class="row mb-4">
                <div class="coolinput col-5">
                    <label for="temperatureSensor" class="text">Temperature Sensor Enabled*</label>
                    <select name="temperatureSensor" id="temperatureSensor" class="input select-input"
                        v-model="formData.temperatureSensor" :class="{ 'placeholder-shown': formData.temperatureSensor === '' }" required>
                        <option disabled value="" class="option-disabled">Select option</option>
                        <option value="true" class="select-options">Yes</option>
                        <option value="false" class="select-options">No</option>
                    </select>
                </div>

                <div class="coolinput col-5">
                    <label for="vibrationSensor" class="text">Vibration Sensor Enabled*</label>
                    <select name="vibrationSensor" id="vibrationSensor" class="input select-input"
                        v-model="formData.vibrationSensor" :class="{ 'placeholder-shown': formData.vibrationSensor === '' }" required>
                        <option disabled value="" class="option-disabled">Select option</option>
                        <option value="true" class="select-options">Yes</option>
                        <option value="false" class="select-options">No</option>
                    </select>
                </div>
            </div>

            <hr>
        </div>
        <!-- Normal Machine Sound -->
        <div>
            <p class="mb-3">Normal Machine Sound</p>
            <div class="row mb-4">
                <div class="coolinput col-10" style="position: relative;">
                    <label for="fileInput" class="text">Upload Normal Sound*</label>
                    <input type="text" :placeholder="normalSoundFile?.name || 'Upload Normal Machine Sound...'" readonly
                        class="upload-input input" disabled />
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

            <!-- Show message when section is not active -->
            <div v-if="!isKnownFaultSectionActive" class="mb-4">
                <p style="color: var(--accent-color3); font-style: italic; text-align: center; padding: 20px;">Click the + button above to add known faulty machine sounds (optional)</p>
            </div>

            <!-- Show input fields when section is active -->
            <div v-if="isKnownFaultSectionActive">
                <div v-for="(fault, index) in knownFaults" :key="fault.id" class="mb-4">
                    <div class="row mb-4">
                        <!-- Fault Name -->
                        <div class="coolinput col-5">
                            <label class="text">Fault Name*</label>
                            <input type="text" placeholder="Add Fault Name..." v-model="fault.name" class="input" :required="isKnownFaultSectionActive" />
                        </div>

                        <!-- File Upload with Filename -->
                        <div class="coolinput col-5" style="position: relative;">
                            <label class="text">Fault Audio*</label>
                            <input type="text" :placeholder="fault.file?.name || 'Upload Fault Sound...'" readonly
                                class="upload-input input" style="padding-right: 80px;" />
                            <button type="button" class="upload-btn" @click="triggerFaultFileUpload(index)" :disabled="fault.uploading">
                                {{ fault.uploading ? 'Uploading...' : 'Upload' }}
                            </button>
                            <input type="file" accept=".mp3,.wav" :ref="el => setFaultFileRef(el, index)" @change="(e) => handleFaultFileUpload(e, index)" style="display: none;" :required="isKnownFaultSectionActive" />
                        </div>
                    </div>

                    <div class="row mb-3">
                        <!-- Description -->
                        <div class="coolinput col-10">
                            <label class="text">Fault Description</label>
                            <textarea placeholder="Write here..." v-model="fault.description" class="input"></textarea>
                        </div>

                        <!-- Remove button (show only if more than one fault) -->
                        <div class="col-2 d-flex align-items-end" v-if="knownFaults.length > 1">
                            <button type="button" @click="removeKnownFault(index)" title="Remove this fault"
                                style="width: 40px; height: 40px; border-radius: 50%; background-color: transparent; color: var(--danger-color); border: none; font-size: 24px; cursor: pointer;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-trash" viewBox="0 0 16 16">
                                    <path
                                        d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z" />
                                    <path
                                        d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <hr />
        </div>

        <div>
            <div class="row mb-4">
                <div class="d-flex justify-content-end gap-2 mt-4">
                    <button type="button" class="button button-primary" @click="submitForm" :disabled="isSubmitting">
                        {{ isSubmitting ? 'Submitting...' : 'Submit' }}
                    </button>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Banner from '../components/banner-component.vue'

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1' // Adjust this to your FastAPI server URL

// Form data
const formData = ref({
    machineName: '',
    manufacturer: '',
    modelNumber: '',
    yearOfInstallation: '',
    operatingHours: null,
    maintenanceSchedule: null,
    lastMaintenanceDate: '',
    expectedLifespan: null,
    temperatureSensor: '',
    vibrationSensor: ''
})

const years = Array.from({ length: 2025 - 1900 + 1 }, (_, i) => 2025 - i);

function checkHours() {
    if (formData.value.operatingHours < 1) formData.value.operatingHours = 1;
    if (formData.value.operatingHours > 24) formData.value.operatingHours = 24;
}

function checkDays() {
    if (formData.value.maintenanceSchedule < 1) formData.value.maintenanceSchedule = 1;
    if (formData.value.maintenanceSchedule > 365) formData.value.maintenanceSchedule = 365;
}

const today = new Date().toISOString().split('T')[0];

// File handling
const normalSoundFile = ref(null);
const hiddenFileInput = ref(null);
const isUploading = ref(false);
const isSubmitting = ref(false);

function triggerFileUpload() {
    hiddenFileInput.value?.click();
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        normalSoundFile.value = file;
    }
}

// Known Faults Section
const isKnownFaultSectionActive = ref(false);
const knownFaults = ref([]);
const faultFileRefs = ref({});
let faultIdCounter = 0;

function addKnownFault() {
    if (!isKnownFaultSectionActive.value) {
        isKnownFaultSectionActive.value = true;
    }
    
    const newFault = {
        id: ++faultIdCounter,
        name: '',
        file: null,
        description: '',
        uploading: false
    };
    
    knownFaults.value.push(newFault);
}

function removeKnownFault(index) {
    const faultId = knownFaults.value[index].id;
    knownFaults.value.splice(index, 1);
    
    delete faultFileRefs.value[faultId];
    
    if (knownFaults.value.length === 0) {
        isKnownFaultSectionActive.value = false;
    }
}

function setFaultFileRef(el, index) {
    if (el && knownFaults.value[index]) {
        faultFileRefs.value[knownFaults.value[index].id] = el;
    }
}

function triggerFaultFileUpload(index) {
    const faultId = knownFaults.value[index].id;
    const fileInput = faultFileRefs.value[faultId];
    if (fileInput) {
        fileInput.click();
    }
}

function handleFaultFileUpload(event, index) {
    const file = event.target.files[0];
    if (file && knownFaults.value[index]) {
        knownFaults.value[index].file = file;
    }
}

// API Functions
async function uploadFile(file, type = 'normal') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);
    
    try {
        const response = await fetch(`${API_BASE_URL}/normal_audio_samples/upload`, {
            method: 'POST',
            body: formData,
        });
        
        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }
        
        const result = await response.json();
        return result.file_path;
    } catch (error) {
        console.error('File upload error:', error);
        throw error;
    }
}

async function createMachine(machineData) {
    try {
        const response = await fetch(`${API_BASE_URL}/machines/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(machineData),
        });
        
        if (!response.ok) {
            throw new Error(`Machine creation failed: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Machine creation error:', error);
        throw error;
    }
}

async function createNormalAudioSample(sampleData) {
    try {
        const response = await fetch(`${API_BASE_URL}/normal_audio_samples/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sampleData),
        });
        
        if (!response.ok) {
            throw new Error(`Normal audio sample creation failed: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Normal audio sample creation error:', error);
        throw error;
    }
}

async function createFault(faultData) {
    try {
        const response = await fetch(`${API_BASE_URL}/faults/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(faultData),
        });
        
        if (!response.ok) {
            throw new Error(`Fault creation failed: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Fault creation error:', error);
        throw error;
    }
}

async function createSensors(machineId, temperatureEnabled, vibrationEnabled) {
    const sensors = [];
    
    if (temperatureEnabled === 'true') {
        sensors.push({
            machine_id: machineId,
            sensor_type: 'temperature',
            is_active: true
        });
    }
    
    if (vibrationEnabled === 'true') {
        sensors.push({
            machine_id: machineId,
            sensor_type: 'vibration',
            is_active: true
        });
    }
    
    const promises = sensors.map(async (sensor) => {
        const response = await fetch(`${API_BASE_URL}/sensors/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sensor),
        });
        
        if (!response.ok) {
            throw new Error(`Sensor creation failed: ${response.statusText}`);
        }
        
        return await response.json();
    });
    
    return await Promise.all(promises);
}

// Validation function - matches exact requirements
function validateForm() {
    const errors = [];
    
    // Always required fields
    if (!formData.value.machineName.trim()) {
        errors.push('Machine Name is required');
    }
    
    if (!formData.value.operatingHours || formData.value.operatingHours < 1 || formData.value.operatingHours > 24) {
        errors.push('Operating Hours per Day is required (1-24)');
    }
    
    if (!formData.value.temperatureSensor) {
        errors.push('Temperature Sensor selection is required');
    }
    
    if (!formData.value.vibrationSensor) {
        errors.push('Vibration Sensor selection is required');
    }
    
    if (!normalSoundFile.value) {
        errors.push('Upload Normal Sound is required');
    }
    
    // Conditional validation - only if user has added faults
    if (isKnownFaultSectionActive.value) {
        knownFaults.value.forEach((fault, index) => {
            if (!fault.name.trim()) {
                errors.push(`Fault Name is required for fault #${index + 1}`);
            }
            if (!fault.file) {
                errors.push(`Fault Audio is required for fault #${index + 1}`);
            }
        });
    }
    
    return errors;
}

// Form submission
async function submitForm() {
    const validationErrors = validateForm();
    
    if (validationErrors.length > 0) {
        alert('Please fix the following errors:\n\n' + validationErrors.join('\n'));
        return;
    }
    
    isSubmitting.value = true;
    
    try {
        // 1. Upload normal sound file
        const normalSoundPath = await uploadFile(normalSoundFile.value, 'normal');
        
        // 2. Create machine
        const machineData = {
            name: formData.value.machineName,
            manufacturer: formData.value.manufacturer || null,
            model_number: formData.value.modelNumber || null,
            year_of_installation: formData.value.yearOfInstallation ? parseInt(formData.value.yearOfInstallation) : null,
            operating_hours_per_day: formData.value.operatingHours,
            maintenance_schedule_days: formData.value.maintenanceSchedule || null,
            last_maintenance_date: formData.value.lastMaintenanceDate || null,
            expected_lifespan_years: formData.value.expectedLifespan || null,
            user_id: 1 // You'll need to get this from your authentication system
        };
        
        const machine = await createMachine(machineData);
        
        // 3. Create normal audio sample
        const normalAudioSampleData = {
            machine_id: machine.id,
            user_id: 1, // You'll need to get this from your authentication system
            file_path: normalSoundPath,
            uploaded_at: new Date().toISOString()
        };
        
        await createNormalAudioSample(normalAudioSampleData);
        
        // 4. Create sensors
        await createSensors(machine.id, formData.value.temperatureSensor, formData.value.vibrationSensor);
        
        // 5. Create known faults if any
        if (isKnownFaultSectionActive.value && knownFaults.value.length > 0) {
            for (const fault of knownFaults.value) {
                const faultSoundPath = await uploadFile(fault.file, 'fault');
                
                const faultData = {
                    machine_id: machine.id,
                    fault_name: fault.name,
                    description: fault.description || null,
                    file_path: faultSoundPath,
                    uploaded_at: new Date().toISOString()
                };
                
                await createFault(faultData);
            }
        }
        
        alert('Machine configuration submitted successfully!');
        
        // Reset form
        resetForm();
        
    } catch (error) {
        console.error('Form submission error:', error);
        alert(`Submission failed: ${error.message}`);
    } finally {
        isSubmitting.value = false;
    }
}

function resetForm() {
    formData.value = {
        machineName: '',
        manufacturer: '',
        modelNumber: '',
        yearOfInstallation: '',
        operatingHours: null,
        maintenanceSchedule: null,
        lastMaintenanceDate: '',
        expectedLifespan: null,
        temperatureSensor: '',
        vibrationSensor: ''
    };
    
    normalSoundFile.value = null;
    isKnownFaultSectionActive.value = false;
    knownFaults.value = [];
    
    // Reset file inputs
    if (hiddenFileInput.value) {
        hiddenFileInput.value.value = '';
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

.add-btn:disabled {
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

.upload-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.upload-input {
    padding: 20px 10px;
}

.button-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
</style>