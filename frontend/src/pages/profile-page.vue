<template>
    <div>
        <Banner />
    </div>
    <div class="card-container ">
        <div class="p-4">
            <div class="mb-4 d-flex align-items-center">
                <h2>Username:</h2>
                <h2 class="user-data mx-4">{{ user && user.username }}</h2>
            </div>

            <div class="mb-4 d-flex align-items-center">
                <h2>Email:</h2>
                <h2 class="user-data mx-4">{{ user && user.email }}</h2>
            </div>

            <div class="mb-4 d-flex align-items-center">
                <h2>Total Machines:</h2>
                <h2 class="user-data mx-4">{{ user && totalMachines }}</h2>
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Banner from '../components/banner-component.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const router = useRouter()

const userId = route.params.userId // make sure your route is /users/:userId
const user = ref(null)
const totalMachines = ref(0)

onMounted(async () => {
  try {
    // Fetch user details
    const userRes = await fetch(`${API_BASE_URL}/users/${userId}`)
    if (!userRes.ok) throw new Error("User not found")
    user.value = await userRes.json()

    // Optionally fetch total machines for this user
    const machineRes = await fetch(`${API_BASE_URL}/machines/user/${userId}`)
    if (machineRes.ok) {
      const machines = await machineRes.json()
      totalMachines.value = machines.length
    } else {
      console.warn("Couldn't fetch machines")
    }

  } catch (error) {
    console.error("Error fetching user data:", error)
    alert("Failed to load user profile.")
    router.push({ name: 'Home' }) // or wherever appropriate
  }
})

function editProfile() {
  console.log('Edit profile clicked')
  router.push({ name: 'EditUser', params: { userId } }) // adjust route name as needed
}

async function deleteProfile() {
  const confirmDelete = confirm("Are you sure you want to delete your profile?")
  if (!confirmDelete) return

  try {
    const res = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'DELETE',
    })

    if (!res.ok) throw new Error("Failed to delete profile")
    alert("Profile deleted successfully.")
    router.push({ name: 'Home' })
  } catch (error) {
    console.error("Error deleting profile:", error)
    alert("Something went wrong.")
  }
}
</script>


<style scoped>
.user-data {
    color: var(--ui-1);
}
</style>