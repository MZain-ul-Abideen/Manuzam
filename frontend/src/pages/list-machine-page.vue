<template>
    <div>
        <Banner />
    </div>

    <div>
        <div class="table-top">
            <h2>List of all Machines</h2>

            <div class="search-container">
                <input type="text" placeholder="Type Machine Name or Model" class="search-input"
                    v-model="searchQuery" />
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="search-icon"
                    viewBox="0 0 16 16">
                    <path
                        d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0" />
                </svg>
            </div>
        </div>


        <!-- Loading state -->
        <div v-if="isLoading" class="text-center py-8">
            Loading machines...
        </div>

        <!-- Error state -->
        <div v-if="error" class="text-center text-red-500 py-8">
            {{ error }}
        </div>

        <!-- Empty state -->
        <div v-if="!isLoading && !error && machines.length === 0" class="text-center py-8">
            No machines found
        </div>

        <!-- Table (only show when not loading and no error) -->
        <div v-if="!isLoading && !error && machines.length > 0" class="table-div text-center">
            <table role="grid">
                <thead class="mb-4">
                    <tr>
                        <th>ID</th>
                        <th>Machine Name</th>
                        <th>Model Number</th>
                        <th>Year of Installation</th>
                        <th class="text-center">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(machine, index) in paginatedMachines" :key="machine.id">
                        <td>{{ machine.id }}</td>
                        <td>{{ machine.name }}</td>
                        <td>{{ machine.model_number }}</td>
                        <td>{{ machine.year_of_installation }}</td>
                        <td class="relative text-center">
                            <button class="menu-btn" @click="toggleMenu(index)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-three-dots-vertical text-white" viewBox="0 0 16 16">
                                    <path
                                        d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0" />
                                </svg>
                            </button>
                            <div v-if="openMenuIndex === index" class="menu-dropdown">
                                <ul>
                                    <li class="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer">
                                        Diagnose</li>
                                    <hr>
                                    <li class="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer"
                                        @click="goToAddAudio(machine.id)">Add Audio</li>
                                    <hr>
                                    <li class="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer"
                                        @click="goToAddSensor(machine.id)">Add Sensor</li>
                                    <hr>
                                    <li class="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer text-danger"
                                        @click="deleteMachine(machine.id)">Delete</li>
                                </ul>
                            </div>

                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-if="!isLoading && !error && machines.length > 0" class="pagination-controls mt-4">
            <div class="pagination-capsule">
                <button class="chevron-left" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-chevron-left" viewBox="0 0 16 16">
                        <path fill-rule="evenodd"
                            d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0" />
                    </svg>
                </button>

                <span class="mx-2">{{ currentPage }} of {{ totalPages }}</span>

                <button class="chevron-right" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-chevron-right" viewBox="0 0 16 16">
                        <path fill-rule="evenodd"
                            d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708" />
                    </svg>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import Banner from '../components/banner-component.vue'
import { getMachines, deleteMachine as deleteMachineApi } from '../services/machineService'

import { useRouter } from 'vue-router'
const router = useRouter()

function goToAddAudio(machineId) {
    router.push({ name: 'AddAudio', params: { machineId } })
}

function goToAddSensor(machineId) {
    router.push({ name: 'AddSensors', params: { machineId } })
}


const machines = ref([])
const isLoading = ref(false)
const error = ref(null)
const openMenuIndex = ref(null)
const currentPage = ref(1)
const pageSize = 10
const searchQuery = ref('')
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Fetch machines on component mount
const fetchMachines = async () => {
    try {
        isLoading.value = true
        error.value = null
        const response = await getMachines()
        machines.value = response
    } catch (err) {
        error.value = 'Failed to fetch machines. Please try again later.'
        console.error('Error fetching machines:', err)
    } finally {
        isLoading.value = false
    }
}

onMounted(() => {
    fetchMachines()
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})

function toggleMenu(index) {
    openMenuIndex.value = openMenuIndex.value === index ? null : index
}

async function deleteMachine(id) {
    if (!confirm('Are you sure you want to delete this machine?')) return

    try {
        openMenuIndex.value = null
        await deleteMachineApi(id)
        await fetchMachines()
    } catch (err) {
        error.value = 'Failed to delete machine. Please try again.'
        console.error('Error deleting machine:', err)
    }
}

function handleClickOutside(event) {
    if (!event.target.closest('.relative')) {
        openMenuIndex.value = null
    }
}

// Computed properties for pagination and filtering
const filteredMachines = computed(() => {
    const query = searchQuery.value.toLowerCase().trim()
    if (!query) return machines.value

    return machines.value.filter(machine =>
        machine.name.toLowerCase().includes(query) ||
        machine.model_number.toLowerCase().includes(query)
    )
})

const totalPages = computed(() => Math.ceil(filteredMachines.value.length / pageSize))

const paginatedMachines = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    const sorted = [...filteredMachines.value].sort((a, b) => b.id - a.id)
    return sorted.slice(start, start + pageSize)
})

function goToPage(page) {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
    }
}

// Reset to first page when search query changes
watch(searchQuery, () => {
    currentPage.value = 1
})
</script>

<style scoped>
.table-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.search-container {
    position: relative;
    display: inline-block;
    width: 250px;
}

.search-input {
    border: 1px solid var(--accent-color3);
    border-radius: 30px;
    color: var(--accent-color1);
    background-color: transparent;
    width: 100%;
    padding: 8px 8px 8px 32px;
    /* extra left padding for icon */
    box-sizing: border-box;
    font-size: var(--body3);
    font-family: Source Sans Pro, sans-serif;
}

.search-icon {
    position: absolute;
    top: 50%;
    left: 10px;
    transform: translateY(-50%);
    color: var(--accent-color1);
    pointer-events: none;
}

.search-input::placeholder {
    font-size: var(--body3);
    font-family: Source Sans Pro, sans-serif;
    color: var(--accent-color1);
}

.search-input:focus {
    outline: none;
    border-color: var(--accent-color1);
}

.table-top h2 {
    color: var(--ui-1);
}

.table-div {
    background: transparent;
    border: none;
    position: relative;
    overflow: visible;
    border: 1px solid var(--accent-color3);
    border-radius: 15px;
    padding: 16px;
}

.table-div table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--body1);
    font-family: Source Sans Pro, sans-serif;
    color: var(--ui-1);
}

th {
    font-weight: 600;
    font-size: var(--body1);
    color: var(--accent-color1);
}

tr {
    border-bottom: 15px solid transparent;
    /* Acts like a gap */
}

td {
    font-weight: 500;
    font-size: var(--body2);
    color: var(--ui-1);
}

.menu-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
}

.menu-dropdown {
    position: absolute;
    background: var(--primary-1);
    z-index: 10;
    border: 1px solid var(--accent-color3);
}

.menu-dropdown ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.menu-dropdown li {
    padding: 8px 16px;
    cursor: pointer;
}

.menu-dropdown li:hover {
    background-color: var(--accent-color1);
}

.menu-dropdown hr {
    margin: 0;
    border: none;
    border-top: 1px solid var(--accent-color3);
}

.pagination-controls {
    display: flex;
    justify-content: center;
    align-items: center;
}

.pagination-capsule {
    border-radius: 2rem;
    width: 250px;
    height: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 2px solid var(--accent-color3);
}

.pagination-controls button {
    background-color: transparent;
    color: var(--accent-color1);
    border: none;
    cursor: pointer;
    width: 20%;
    height: 100%;
}

.pagination-controls button:disabled {
    cursor: not-allowed;
    color: var(--secondary-1);

}

.chevron-left {
    border-right: 1px solid var(--accent-color3) !important;
}

.chevron-right {
    border-left: 1px solid var(--accent-color3) !important;
}
</style>