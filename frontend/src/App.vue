<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidenav from './components/sidenav-component.vue'

const route = useRoute()

const hideSidebar = computed(() => {
  return route.path === '/login' || route.path === '/register' || route.name === 'NotFound'
})

</script>

<template>
  <div class="row">
    <div v-if="!hideSidebar" class="col-1">
      <Sidenav />
    </div>


    <div :class="hideSidebar ? 'col-12' : 'col-11 pt-5 px-5'">
      <router-view />
    </div>
  </div>
</template>



<style scoped></style>
