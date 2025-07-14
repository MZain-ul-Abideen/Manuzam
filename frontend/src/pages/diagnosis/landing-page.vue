<!-- frontend/src/pages/diagnosis/landing-page.vue -->
<template>
    <div class="row">
        <div class="col-6">

            <div class="landing-page">

                <div class="intro-section">
                    <h1 class="title">Smarter Maintenance. Safer Machines. Seamless Operations.</h1>
                    <p class="subtitle">
                        Manuzam is an intelligent platform designed to monitor, diagnose, and optimize industrial
                        machines in real-time. By combining sensor data, predictive maintenance algorithms, and
                        user-friendly dashboards, Manuzam helps businesses reduce downtime, detect anomalies early, and
                        ensure smooth, efficient operations across all equipment.
                    </p>

                    <div class="button-group">
                        <button class="button button-secondary" @click="goToAddMachine">Create a Machine</button>
                        <button class="button button-primary" @click="goToTraining">Train or Diagnose</button>
                    </div>
                </div>
            </div>
        </div>


        <div class="col-6 d-flex justify-content-center align-items-center">
            <img src="@/assets/landingpage-img.png" alt="" class="img-fluid" />
        </div>
    </div>

</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goToTraining() {
    router.push({ name: 'ListMachine' })
}

function goToAddMachine() {
    router.push({ name: 'AddMachine' })
}
</script>

<style scoped>
.landing-page {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.intro-section {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.title {
    font-size: 3.2rem;
    font-weight: 700;
    color: var(--accent-color1);
    margin-top: 10rem;
    margin-bottom: 1rem;
}

.subtitle {
    font-size: var(--body1);
    color: var(--ui-1);
    margin-bottom: 2.5rem;
}

.button-group {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 3rem;
}

.img-fluid {
    width: 29rem;
    height: auto;
}
</style>