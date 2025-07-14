<!-- frontend/src/pages/diagnosis/dashboard-page.vue -->
<template>

  <PredictPage/>
  
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import PredictPage from '@/pages/diagnosis/dashboard/predict-page.vue'
import ResultPage from '@/pages/diagnosis/dashboard/result-page.vue'
</script>