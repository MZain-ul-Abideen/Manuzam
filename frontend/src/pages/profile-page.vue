<template>
    <div>
        <Banner />
    </div>
    <div class="card-container ">
        <div class="p-4">
            <div class="mb-4 d-flex align-items-center">
                <h2>Username:</h2>
                <h2 class="user-data mx-4">{{ user.username }}</h2>
            </div>

            <div class="mb-4 d-flex align-items-center">
                <h2>Email:</h2>
                <h2 class="user-data mx-4">{{ user.email }}</h2>
            </div>

            <div class="mb-4 d-flex align-items-center">
                <h2>Total Machines:</h2>
                <h2 class="user-data mx-4">{{ totalMachines }}</h2>
            </div>

            <hr>

            <div class="d-flex justify-content-end gap-2 mt-5">
                <button class="button button-secondary" @click="editProfile">Edit</button>
                <button class="button button-danger" @click="deleteProfile">Delete</button>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import Banner from '../components/banner-component.vue'

// Mock user data – replace with real data or API
const user = ref({
    username: 'Zain Khan',
    email: 'zain@example.com',
})

// Replace with actual machine count (from props or API)
const totalMachines = ref(5)

function editProfile() {
    console.log('Edit profile clicked')
    // You can navigate to an edit page or open a modal
}

function deleteProfile() {
    console.log('Delete profile clicked')
    // Add confirmation and delete logic here
}
</script>

<style scoped>
.user-data {
    color: var(--ui-1);
}
</style>