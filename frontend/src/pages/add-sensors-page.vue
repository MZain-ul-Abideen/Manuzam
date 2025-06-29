<template>
  <div>
    <Banner />
  </div>
  <div class="card-container">
    <!-- Sensor Configuration -->
    <div>
      <p class="mb-3">Sensor Configuration</p>
      <div class="row mb-4">
        <div class="d-flex flex-column col-5">
          <div class="coolinput">
            <label for="temperatureSensor" class="text">Temperature Sensor Enabled*</label>
            <select name="temperatureSensor" id="temperatureSensor" class="input select-input" required
              v-model="temperatureSensorEnabled">
              <option disabled value="" class="option-disabled" selected>Select option</option>
              <option value="true" class="select-options">Yes</option>
              <option value="false" class="select-options">No</option>
            </select>
            <p class="mt-2 text-danger" v-if="errors.temperatureSensor">{{ errors.temperatureSensor }}</p>
          </div>
          <div class="coolinput mt-3" v-if="temperatureSensorEnabled === 'true'">
            <label for="temperatureName" class="text">Add Temperature Sensor Value</label>
            <input type="number" placeholder="Write Temperature in number..." name="temperatureName"
              id="temperatureName" class="input" v-model="temperatureValue">
            <p class="mt-2 text-danger" v-if="errors.temperatureValue">{{ errors.temperatureValue }}</p>
          </div>
        </div>

        <div class="d-flex flex-column col-5">
          <div class="coolinput">
            <label for="vibrationSensor" class="text">Vibration Sensor Enabled*</label>
            <select name="vibrationSensor" id="vibrationSensor" class="input select-input" required
              v-model="vibrationSensorEnabled">
              <option disabled value="" class="option-disabled" selected>Select option</option>
              <option value="true" class="select-options">Yes</option>
              <option value="false" class="select-options">No</option>
            </select>
            <span class="mt-2 text-danger" v-if="errors.vibrationSensor">{{ errors.vibrationSensor }}</span>
          </div>
          <div class="coolinput mt-3" v-if="vibrationSensorEnabled === 'true'">
            <label for="vibration" class="text">Vibration Sensor Value</label>
            <input type="number" placeholder="Write Vibration in number..." name="vibration" id="vibration"
              class="input" v-model="vibrationValue">
            <span class="mt-2 text-danger" v-if="errors.vibrationValue">{{ errors.vibrationValue }}</span>
          </div>
        </div>
      </div>

    </div>

    <div>
      <div class="row mb-4">
        <div class="d-flex justify-content-end gap-2 mt-4">
          <button type="button" class="button button-primary" @click="submitSensorData">
            Submit
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import Banner from '../components/banner-component.vue'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const machineId = route.params.machineId
const machine = ref(null)
const router = useRouter()

// State to track dropdown selections
const temperatureSensorEnabled = ref('')
const vibrationSensorEnabled = ref('')
const temperatureValue = ref(null)
const vibrationValue = ref(null)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const errors = ref({
  temperatureSensor: '',
  temperatureValue: '',
  vibrationSensor: '',
  vibrationValue: ''
})



onMounted(async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/machines/${machineId}`)
    if (!response.ok) throw new Error('Machine not found')
    machine.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch machine:', error)
    // optionally redirect or show error UI
  }
})

const submitSensorData = async () => {
  // Reset all errors
  errors.value = {
    temperatureSensor: '',
    temperatureValue: '',
    vibrationSensor: '',
    vibrationValue: ''
  };

  let isValid = true;

  // Validate dropdowns
  if (!temperatureSensorEnabled.value) {
    errors.value.temperatureSensor = 'Please select if temperature sensor is enabled';
    isValid = false;
  }
  if (!vibrationSensorEnabled.value) {
    errors.value.vibrationSensor = 'Please select if vibration sensor is enabled';
    isValid = false;
  }

  // Validate temperature value if enabled
  if (temperatureSensorEnabled.value === 'true') {
    if (temperatureValue.value === null || temperatureValue.value === '') {
      errors.value.temperatureValue = 'Temperature value is required';
      isValid = false;
    }
  }

  // Validate vibration value if enabled
  if (vibrationSensorEnabled.value === 'true') {
    if (vibrationValue.value === null || vibrationValue.value === '') {
      errors.value.vibrationValue = 'Vibration value is required';
      isValid = false;
    }
  }

  if (!isValid) {
    return alert('Please fill out the form correctly before submitting.');
  }

  // If valid, proceed to API call
  const payload = {
    machine_id: Number(machineId),
    temperature_sensor_enabled: temperatureSensorEnabled.value === 'true',
    vibration_sensor_enabled: vibrationSensorEnabled.value === 'true',
    temperature_value: temperatureSensorEnabled.value === 'true' ? parseFloat(temperatureValue.value) : null,
    vibration_value: vibrationSensorEnabled.value === 'true' ? parseFloat(vibrationValue.value) : null
  };

  try {
    const response = await fetch(`${API_BASE_URL}/sensors/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || 'Failed to create sensor data');
    }

    const result = await response.json();
    console.log('Sensor created:', result);
    alert('Sensor data submitted successfully!');
    router.push({ name: 'ListMachine' });

  } catch (error) {
    console.error('Error:', error);
    alert(`Submission failed: ${error.message}`);
  }
};

</script>