<template>
    <div>
        <Banner />
    </div>

    <div>
    </div>
</template>

<script setup>
import Banner from '../components/banner-component.vue'


import { ref, onMounted } from 'vue';
  import { getUsers } from '../services/userService';
  
  const users = ref([]);
  
  onMounted(async () => {
    users.value = await getUsers();
  });
</script>