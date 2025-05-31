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


        <div class="table-div text-center">
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
                    <tr v-for="(machine, index) in paginatedMachines" :key="(currentPage - 1) * pageSize + index">
                        <td>{{ machine.id }}</td>
                        <td>{{ machine.name }}</td>
                        <td>{{ machine.model }}</td>
                        <td>{{ machine.year }}</td>
                        <td class="relative text-center">
                            <button class="menu-btn" @click="toggleMenu(index)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-three-dots-vertical text-white" viewBox="0 0 16 16">
                                    <path
                                        d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0" />
                                </svg> </button>
                            <div v-if="openMenuIndex === index" class="menu-dropdown">
                                <ul>
                                    <li class="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer"
                                        @click="editMachine(index)">Diagnose</li>
                                    <hr>
                                    <li class="px-4 py-2 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer"
                                        @click="deleteMachine(machine.id)">Delete</li>
                                </ul>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="pagination-controls mt-4">
            <div class="pagination-capsule">
                <button class="chevron-left" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-chevron-left" viewBox="0 0 16 16">
                        <path fill-rule="evenodd"
                            d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0" />
                    </svg> </button>

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
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import Banner from '../components/banner-component.vue'

const machines = reactive([
    { id: '1', name: 'Machine 1', model: 'GRE12432', year: '2017' },
    { id: '2', name: 'Machine 2', model: 'FD243242', year: '2020' },
    { id: '3', name: 'Machine 3', model: 'VDV2313', year: '2025' },
    { id: '4', name: 'Machine 4', model: 'GBF32421', year: '2017' },
    { id: '5', name: 'Machine 5', model: 'FS412321', year: '2002' },
    { id: '6', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '7', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '8', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '9', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '10', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '11', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '12', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '13', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '14', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '15', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '16', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '17', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '18', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '19', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '20', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '21', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '22', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '23', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '24', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '25', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '26', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '27', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '28', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '29', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '30', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '31', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '32', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '33', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '34', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '35', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '36', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '37', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '38', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '39', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '41', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '42', name: 'Machine 6', model: 'JMK23124', year: '2020' },
    { id: '43', name: 'Machine 16', model: 'JMK23124', year: '2020' },
])

const openMenuIndex = ref(null)

function toggleMenu(index) {
    // If clicking the same menu, close it. Otherwise, open the new one
    openMenuIndex.value = openMenuIndex.value === index ? null : index
}

function editMachine(index) {
    openMenuIndex.value = null
}

function deleteMachine(id) {
    openMenuIndex.value = null
    const idx = machines.findIndex(m => m.id === id)
    if (idx !== -1) machines.splice(idx, 1)
}


function handleClickOutside(event) {
    if (!event.target.closest('.relative')) {
        openMenuIndex.value = null
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})

const currentPage = ref(1)
const pageSize = 15

const totalPages = computed(() => Math.ceil(filteredMachines.value.length / pageSize))

const paginatedMachines = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return filteredMachines.value.slice(start, start + pageSize)
})

function goToPage(page) {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
    }
}

const searchQuery = ref('')

const filteredMachines = computed(() => {
    const query = searchQuery.value.toLowerCase().trim()
    if (!query) return machines

    return machines.filter(machine =>
        machine.name.toLowerCase().includes(query) ||
        machine.model.toLowerCase().includes(query)
    )
})

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