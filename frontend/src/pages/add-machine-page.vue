<template>
    <div>
        <Banner />
    </div>
    <div class="card-container">
        <div>
            <p class="mb-3">Basic Info</p>
            <div class="row mb-4">
                <div class="coolinput col-5">
                    <label for="input" class="text">Machine Name*</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div><!-- From Uiverse.io by kamehame-ha -->
                <div class="coolinput col-5">
                    <label for="input" class="text">Manufacturer</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div>
            </div>
            <div class="row mb-5">
                <div class="coolinput col-5">
                    <label for="input" class="text">Model Number</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div><!-- From Uiverse.io by kamehame-ha -->
                <div class="coolinput col-5">
                    <label for="input" class="text">Year of Installation</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div>
            </div>
            <hr>
        </div>
        <div>
            <p class="mb-3">Operational Details</p>
            <div class="row mb-4">
                <div class="coolinput col-5">
                    <label for="input" class="text">Operating Hours per Day*</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div><!-- From Uiverse.io by kamehame-ha -->
                <div class="coolinput col-5">
                    <label for="input" class="text">Maintenance Schedule</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div>
            </div>
            <div class="row mb-5">
                <div class="coolinput col-5">
                    <label for="input" class="text">Last Maintenance Date</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div><!-- From Uiverse.io by kamehame-ha -->
                <div class="coolinput col-5">
                    <label for="input" class="text">Expected Lifespan</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div>
            </div>
            <hr>
        </div>
        <div>
            <p class="mb-3">Sensor Configuration</p>
            <div class="row mb-4">
                <div class="coolinput col-5">
                    <label for="input" class="text">Temperature Sensor Enabled*</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div><!-- From Uiverse.io by kamehame-ha -->
                <div class="coolinput col-5">
                    <label for="input" class="text">Vibration Sensor Enabled*</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div>
            </div>
            <hr>
        </div>
        <div>
            <p class="mb-3">Normal Machine Sound</p>
            <div class="row mb-4">
                <div class="coolinput col-10">
                    <label for="input" class="text">Upload Normal Sound*</label>
                    <input type="text" placeholder="Write here..." name="input" class="input">
                </div>
            </div>
            <hr>
        </div>
        <div>
            <div class="d-flex justify-content-between align-items-center mb-3">
                <p>Known faulty Machine Sound</p>
                <button class="add-btn" @click="addFault">+</button>
            </div>

            <div v-for="(fault, index) in faults" :key="index" class="row mb-4">
                <div class="coolinput col-5">
                    <label class="text">Fault Name*</label>
                    <input type="text" placeholder="Write here..." v-model="fault.name" class="input" />
                </div>
                <div class="coolinput col-5">
                    <label class="text">Fault Audio*</label>
                    <input type="text" placeholder="Write here..." v-model="fault.audio" class="input" />
                </div>
                <div class="coolinput col-10 mt-3">
                    <label class="text">Fault Description</label>
                    <textarea placeholder="Write here..." v-model="fault.description" class="input"></textarea>
                </div>
            </div>
            <hr>

        </div>

        <div>
            <div class="row mb-4">
                <div class="d-flex justify-content-end gap-2 mt-4">
                    <button class="button button-secondary" @click="editProfile">Back</button>
                    <button class="button button-primary" @click="deleteProfile">Submit</button>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import Banner from '../components/banner-component.vue'
import { ref } from 'vue'

const faults = ref([])

function addFault() {
    faults.value.push({
        name: '',
        audio: '',
        description: ''
    })
}
</script>

<style scoped>
.add-btn {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: transparent;
    color: var(--accent-color1);
    border: 2px solid var(--accent-color1);
    font-size: 32px;
    cursor: pointer;
}
</style>