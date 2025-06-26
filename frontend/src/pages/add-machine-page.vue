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
                    <input type="text" required placeholder="Write Machine Name..." name="machineName" id="machineName"
                        class="input" v-model="formData.machineName">
                </div>
                <div class="coolinput col-5">
                    <label for="manufacturer" class="text">Manufacturer</label>
                    <input type="text" placeholder="Write Manufacturer..." name="manufacturer" id="manufacturer"
                        class="input" v-model="formData.manufacturer">
                </div>
            </div>
            <div class="row mb-5">
                <div class="coolinput col-5">
                    <label for="modelNumber" class="text">Model Number</label>
                    <input type="text" placeholder="Add Model Number..." name="modelNumber" id="modelNumber"
                        class="input" v-model="formData.modelNumber">
                </div>
                <div class="coolinput col-5">
                    <label for="yearOfInstallation" class="text">Year of Installation</label>
                    <select v-model="formData.yearOfInstallation" name="yearOfInstallation" id="yearOfInstallation"
                        class="input select-input" :class="{ 'placeholder-shown': formData.yearOfInstallation === '' }">
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
                        placeholder="Enter hours from 1 to 24..." min="1" max="24"
                        v-model.number="formData.operatingHours" @input="checkHours" required>
                </div>

                <div class="coolinput col-5">
                    <label for="maintenanceSchedule" class="text">Maintenance Schedule</label>
                    <input type="number" name="maintenanceSchedule" id="maintenanceSchedule" class="input" min="1"
                        max="365" placeholder="Enter days from 1 to 365..."
                        v-model.number="formData.maintenanceSchedule" @input="checkDays" />
                </div>
            </div>
            <div class="row mb-5">
                <div class="coolinput col-5">
                    <label for="lastMaintenanceDate" class="text">Last Maintenance Date</label>
                    <input type="date" id="lastMaintenanceDate" name="lastMaintenanceDate" :max="today"
                        v-model="formData.lastMaintenanceDate" class="input"
                        :class="{ empty: !formData.lastMaintenanceDate }" />
                </div>
                <div class="coolinput col-5">
                    <label for="expectedLifespan" class="text">Expected Lifespan</label>
                    <input type="number" min="1" placeholder="Enter Years e.g., 10..." name="expectedLifespan"
                        id="expectedLifespan" v-model="formData.expectedLifespan" class="input">
                </div>

            </div>
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
import { ref } from 'vue'
import Banner from '../components/banner-component.vue'
import { createMachine } from '../services/machineService'
import { useRouter } from 'vue-router'

const router = useRouter()

const formData = ref({
    machineName: '',
    manufacturer: '',
    modelNumber: '',
    yearOfInstallation: '',
    operatingHours: null,
    maintenanceSchedule: '',
    lastMaintenanceDate: '',
    expectedLifespan: null
})

const years = Array.from({ length: 2025 - 1900 + 1 }, (_, i) => 2025 - i)
const today = new Date().toISOString().split('T')[0]
const isSubmitting = ref(false)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function checkHours() {
    if (formData.value.operatingHours < 1) formData.value.operatingHours = 1
    if (formData.value.operatingHours > 24) formData.value.operatingHours = 24
}

function submitForm() {
    if (!formData.value.machineName.trim()) {
        alert('Machine Name is required')
        return
    }

    if (
        !formData.value.operatingHours ||
        formData.value.operatingHours < 1 ||
        formData.value.operatingHours > 24
    ) {
        alert('Operating Hours must be between 1 and 24')
        return
    }

    isSubmitting.value = true

    const machineData = {
        name: formData.value.machineName,
        manufacturer: formData.value.manufacturer || '',
        model_number: formData.value.modelNumber || '',
        year_of_installation: formData.value.yearOfInstallation
            ? parseInt(formData.value.yearOfInstallation)
            : null,
        operating_hours_per_day: formData.value.operatingHours,
        maintenance_schedule: formData.value.maintenanceSchedule?.toString() || '0',  // ✅ as string
        last_maintenance_date: formData.value.lastMaintenanceDate || null,
        expected_lifespan: formData.value.expectedLifespan || 0, // ✅ fix field name
        user_id: 1 // Replace with actual user id
    }


    createMachine(machineData)
        .then(() => {
            alert('Machine created successfully!')
            router.push({ name: 'ListMachine' });
        })
        .catch(error => {
            alert(`Submission failed: ${error.message}`)
            console.error(error)
        })
        .finally(() => {
            isSubmitting.value = false
        })
}
</script>