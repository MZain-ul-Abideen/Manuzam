<template>
    <div class="wrapper">
        <h1 class="hero-heading">404</h1>
        <p class="">Page Not Found</p>
        <button class="button button-primary mt-4">
            <router-link to="/" class="">Go back to Home</router-link>
        </button>
    </div>
</template>

<style scoped>
.wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 100vh;
}
</style>