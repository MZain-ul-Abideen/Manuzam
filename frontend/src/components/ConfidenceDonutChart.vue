<template>
  <div class="donut-container">
    <Doughnut :data="chartData" :options="chartOptions" />
    <div class="center-text">
      {{ Math.round(confidence * 100) }}%
    </div>
  </div>
</template>

<script setup>
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  confidence: {
    type: Number,
    required: true
  }
})

const chartData = {
  labels: ['Confidence', 'Remaining'],
  datasets: [
    {
      data: [props.confidence, 1 - props.confidence],
      backgroundColor: ['#1DB954', '#EEEEEE'],
      borderWidth: 0,
      hoverOffset: 4
    }
  ]
}

const chartOptions = {
  cutout: '80%',
  animation: {
    animateRotate: true,
    duration: 1200,
    easing: 'easeOutBounce'
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      enabled: false
    }
  }
}
</script>

<style scoped>
.donut-container {
  position: relative;
  width: 200px;
  height: 200px;
  margin: auto;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}

.center-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--accent-color1);
}
</style>
