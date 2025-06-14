<template>
    <div>
        <Banner />
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="text-center py-8">
        Loading Users...
    </div>

    <div>
        <div class="table-top">
            <h2>List of all Users</h2>

            <div class="search-container">
                <input type="text" placeholder="Search by username or email" class="search-input"
                    v-model="searchQuery" />
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="search-icon"
                    viewBox="0 0 16 16">
                    <path
                        d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0" />
                </svg>
            </div>
        </div>

        <!-- Error state -->
        <div v-if="error" class="text-center text-red-500 py-8">
            {{ error }}
        </div>

        <!-- Empty state -->
        <div v-if="!isLoading && !error && users.length === 0" class="text-center py-8">
            No Users found
        </div>

        <!-- Table (only show when not loading and no error) -->
        <div v-if="!isLoading && !error && users.length > 0" class="table-div text-center">
            <table role="grid">
                <thead class="mb-4">
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th class="text-center">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(user, index) in paginatedUsers" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td class="relative text-center">
                            <button class="menu-btn" @click="deleteUser(user.id)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-trash" viewBox="0 0 16 16">
                                    <path
                                        d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z" />
                                    <path
                                        d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z" />
                                </svg>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-if="!isLoading && !error && users.length > 0" class="pagination-controls mt-4">
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
import { ref, computed, onMounted, watch } from 'vue'
import Banner from '../components/banner-component.vue'
import { getUsers, deleteUser as deleteUserApi } from '../services/userService'

const users = ref([])
const isLoading = ref(false)
const error = ref(null)
const currentPage = ref(1)
const pageSize = 10
const searchQuery = ref('')

// Fetch users on component mount
const fetchUsers = async () => {
    try {
        isLoading.value = true
        error.value = null
        const response = await getUsers()
        users.value = response
    } catch (err) {
        error.value = 'Failed to fetch users. Please try again later.'
        console.error('Error fetching users:', err)
    } finally {
        isLoading.value = false
    }
}

onMounted(() => {
    fetchUsers()
})

async function deleteUser(id) {
    if (!confirm('Are you sure you want to delete this user?')) return

    try {
        await deleteUserApi(id)
        await fetchUsers()
    } catch (err) {
        error.value = 'Failed to delete user. Please try again.'
        console.error('Error deleting user:', err)
    }
}

// Computed properties for pagination and filtering
const filteredUsers = computed(() => {
    const query = searchQuery.value.toLowerCase().trim()
    if (!query) return users.value

    return users.value.filter(user =>
        user.username.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query)
    )
})

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / pageSize))

const paginatedUsers = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return filteredUsers.value.slice(start, start + pageSize)
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
    color: var(--ui-1);
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