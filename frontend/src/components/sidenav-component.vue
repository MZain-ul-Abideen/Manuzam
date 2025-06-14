<template>
  <div class="side-nav-bg">
    <div class="side-nav">
      <!-- Navigation Links -->
      <nav class="flex-grow-1 mt-5">
        <ul class="nav flex-column">
          <li
            class="d-flex justify-content-center mt-3 mb-4"
            v-for="(link, index) in navLinks"
            :key="index"
          >
            <router-link
              class="nav-link p-2 d-flex align-items-center justify-content-center"
              :to="link.to"
              :title="link.alt"
              :class="{ active: route.path === link.to }"
            >
              <img :src="link.icon" :alt="link.alt" width="24" height="24" />
            </router-link>
          </li>
        </ul>
      </nav>

      <hr />

      <!-- Logout Button -->
      <div class="nav flex-column mb-3">
        <div class="d-flex justify-content-center mt-3 mb-4">
          <router-link
            class="nav-link p-2 d-flex align-items-center justify-content-center"
            :to="'/logout'" 
            title="Logout"
          >
            <img :src="logoutIcon" alt="Logout" width="24" height="24" />
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>



<script setup>
import { useRoute, useRouter } from 'vue-router'
import dashboardIcon from '../assets/sidenav-icons/dashboard.svg'
import diagnosisIcon from '../assets/sidenav-icons/diagnosis.svg'
import logoutIcon from '../assets/sidenav-icons/logout.svg'
import addmachineIcon from '../assets/sidenav-icons/machine-add.svg'
import machinelistIcon from '../assets/sidenav-icons/machine-list.svg'

const navLinks = [
  { icon: dashboardIcon, alt: 'Dashboard', to: '/dashboard' },
  { icon: diagnosisIcon, alt: 'Diagnosis', to: '/diagnosis' },
  { icon: machinelistIcon, alt: 'Machine List', to: '/list_machines' },
  { icon: addmachineIcon, alt: 'Add Machine', to: '/AddMachine' },
]

const route = useRoute()
</script>


<style scoped>

.side-nav-bg {
  background: transparent;
  height: 100vh;
  padding: 1.5em;
}

.side-nav {
  background: var(--accent-color2) !important;
  height: 100%;
  border-radius: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 1rem;
}

.nav-link {
  border-radius: 12px;
  width: 48px;
  height: 48px;
  transition: background 0.3s ease;
}

.nav-link.active {
  background: var(--accent-color3);
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
}

hr {
  border: none;
  border-top: 1px solid white;
  opacity: 0.5;
  width: 60%;
  margin: 1rem auto;
}


</style>