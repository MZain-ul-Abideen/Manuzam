<template>
  <Banner :machineName="machine?.name || ''" />
  <div class="result-page" v-if="prediction">

    <div class="row major-card-wrapper">
      <div class="col-md-12 major-card">
        <div class="col-9 major-card-text">
          <h1 class="m-0">{{ audioTitleHeading }}</h1>
          <span class="file-name">{{ fileName }}</span>
          <p v-if="faultDescription">{{ faultDescription }}</p>
          <p v-else-if="normalTitle">{{ normalTitle }}</p>
        </div>

        <div class="col-3 major-card-cart">
          <ConfidenceDonutChart v-if="prediction?.confidence_scores"
            :confidence="prediction.confidence_scores[prediction.predicted_label]" />
          <div class="major-card-stats">
            <h4>
              Confidence Score:
              {{ prediction.confidence_scores[prediction.predicted_label]?.toFixed(2) }}
            </h4>
            <p v-if="isLowConfidence" class="low-confidence-warning">
              ⚠️ Model not certain — this might be a new or unseen fault.
            </p>
          </div>

        </div>
      </div>
    </div>

    <!-- Temperature / Vibration Cards -->
    <div class="row minor-card-wrapper">
      <!-- Temperature -->
      <div class="col-6 minor-card-div minor-card-left">
        <div class="minor-card">
          <h1>Temperature</h1>
          <span class="big">
            {{ temperature }}/<span class="small">
              {{ avgTemperature !== 'N/A' ? avgTemperature.toFixed(2) : 'N/A' }} AVG
            </span>
          </span>
          <h5 :class="temperatureColor">{{ temperatureWarning }}</h5>
        </div>
      </div>

      <!-- Vibration -->
      <div class="col-6 minor-card-div minor-card-right">
        <div class="minor-card">
          <h1>Vibration</h1>
          <span class="big">
            {{ vibration }}/<span class="small">
              {{ avgVibration !== 'N/A' ? avgVibration.toFixed(2) : 'N/A' }} AVG
            </span>
          </span>
          <h5 :class="vibrationColor">{{ vibrationWarning }}</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import ConfidenceDonutChart from '@/components/ConfidenceDonutChart.vue'
import Banner from '@/components/banner-component.vue'

const route = useRoute()
const router = useRouter()

const prediction = ref(null)
const fileName = ref('')
const temperature = ref('N/A')
const vibration = ref('N/A')
const avgTemperature = ref('N/A')
const avgVibration = ref('N/A')
const faultDescription = ref('')
const normalTitle = ref('')
const machine = ref(null) // ✅ For machine name

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

onMounted(async () => {
  const stored = sessionStorage.getItem('predictionResult')
  if (!stored) {
    router.replace({ name: 'PredictPage', params: { machineId: route.params.machineId } })
    return
  }

  const parsed = JSON.parse(stored)
  prediction.value = parsed.result
  fileName.value = parsed.fileName
  temperature.value = parsed.temperature ?? 'N/A'
  vibration.value = parsed.vibration ?? 'N/A'

  try {
    const sensorRes = await fetch(`${API_BASE_URL}/sensors/machine/${route.params.machineId}`)
    if (sensorRes.ok) {
      const sensor = await sensorRes.json()
      avgTemperature.value = sensor?.temperature_value ?? 'N/A'
      avgVibration.value = sensor?.vibration_value ?? 'N/A'
    }
  } catch (error) {
    console.error('Failed to fetch sensor averages:', error)
  }

  // ✅ Fetch machine info to show name in banner
  try {
    const machineRes = await fetch(`${API_BASE_URL}/machines/${route.params.machineId}`)
    if (machineRes.ok) {
      machine.value = await machineRes.json()
    }
  } catch (error) {
    console.error('Failed to fetch machine name:', error)
  }

  const label = prediction.value.predicted_label.toLowerCase()

  if (label === 'normal') {
    try {
      const normalRes = await fetch(`${API_BASE_URL}/normal_audio_samples/machine/${route.params.machineId}`)
      if (normalRes.ok) {
        const normalSamples = await normalRes.json()
        normalTitle.value = normalSamples[0]?.title ?? ''
      }
    } catch (error) {
      console.error('Failed to fetch normal audio title:', error)
    }
  } else {
    try {
      const faultsRes = await fetch(`${API_BASE_URL}/faults/machine/${route.params.machineId}`)
      if (faultsRes.ok) {
        const faults = await faultsRes.json()
        const fault = faults.find(f => f.name.toLowerCase().trim() === label.trim())
        faultDescription.value = fault?.description ?? ''
      }
    } catch (error) {
      console.error('Failed to fetch faults:', error)
    }
  }
})

const audioTitleHeading = computed(() => {
  if (prediction.value?.predicted_label?.toLowerCase() === 'normal') {
    return 'Normal Machine Audio'
  }
  return prediction.value?.predicted_label || 'Unknown'
})


const temperatureWarning = computed(() => {
  if (temperature.value === 'N/A' || avgTemperature.value === 'N/A') return 'N/A'

  const t = parseFloat(temperature.value)
  const avg = parseFloat(avgTemperature.value)

  if (Math.abs(t - avg) < 2) return 'Normal'
  if (t > avg + 10) return 'Too High!'
  if (t > avg + 5) return 'High'
  if (t < avg - 10) return 'Too Low!'
  if (t < avg - 5) return 'Low'

  return 'Slightly Off'
})

const temperatureColor = computed(() => {
  if (temperature.value === 'N/A' || avgTemperature.value === 'N/A') return 'neutral'

  const t = parseFloat(temperature.value)
  const avg = parseFloat(avgTemperature.value)
  const diff = t - avg

  if (diff < -10) return 'blue'
  if (diff < -5) return 'grey'
  if (Math.abs(diff) <= 2) return 'grey'
  if (diff > 10) return 'red'
  if (diff > 5) return 'orange'
  return 'yellow'
})


const vibrationWarning = computed(() => {
  if (vibration.value === 'N/A' || avgVibration.value === 'N/A') return 'N/A'

  const v = parseFloat(vibration.value)
  const avg = parseFloat(avgVibration.value)

  if (Math.abs(v - avg) < 0.2) return 'Normal'
  if (v > avg + 1) return 'Too High!'
  if (v > avg + 0.5) return 'High'
  if (v < avg - 1) return 'Too Low!'
  if (v < avg - 0.5) return 'Low'

  return 'Slightly Off'
})

const vibrationColor = computed(() => {
  if (vibration.value === 'N/A' || avgVibration.value === 'N/A') return 'neutral'

  const v = parseFloat(vibration.value)
  const avg = parseFloat(avgVibration.value)
  const diff = v - avg

  if (diff < -1) return 'blue'
  if (diff < -0.5) return 'grey'
  if (Math.abs(diff) <= 0.2) return 'grey'
  if (diff > 1) return 'red'
  if (diff > 0.5) return 'orange'
  return 'yellow'
})

const isLowConfidence = computed(() => {
  if (!prediction.value || !prediction.value.confidence_scores) return false

  const label = prediction.value.predicted_label
  const score = prediction.value.confidence_scores[label]

  return score !== undefined && score < 0.6
})


</script>


<style scoped>
.file-name {
  font-size: 1.5rem;
  color: #7e7e7e;
  font-family: Source Sans Pro, sans-serif;
}

.result-page {
  width: 100%;
  height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.major-card-wrapper {
  width: 100%;
  height: 50%;
  margin-bottom: 25px;
}

.major-card {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  border: 1px solid var(--accent-color1);
  border-radius: 20px;
}

.major-card-text {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 5rem;
}

.major-card-cart {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.major-card-cart-diagram img {
  width: 100%;
  height: 80%;
}

.major-card-stats {
  width: 100%;
  height: 20%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: white;
}

.minor-card-wrapper {
  width: 100%;
  height: 50%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.minor-card-div {
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.minor-card {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  border: 1px solid var(--accent-color1);
  border-radius: 20px;
}

.minor-card .big {
  font-size: 5rem;
  color: var(--ui-1);
}

.minor-card .small {
  font-size: 2rem;
  color: var(--ui-1);
}

.minor-card-left {
  padding-right: 10px;
}

.minor-card-right {
  padding-left: 10px;
}

.low-confidence-warning {
  margin-top: 8px;
  font-size: 1rem;
  color: var(--danger-color);
  /* deep orange */
  font-weight: bold;
  text-align: center;
}


.blue {
  color: #057fe2;
  /* blue */
}

.grey {
  color: #9e9e9e;
  /* grey */
}

.yellow {
  color: #ffeb3b;
  /* yellow */
}

.orange {
  color: #ff9800;
  /* orange */
}

.red {
  color: #d81709;
  /* red */
}

.neutral {
  color: #b0bec5;
  /* fallback greyish */
}
</style>