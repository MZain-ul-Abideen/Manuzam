<template>
    <div class="signin-wrapper">
        <div class="signin-card ">
            <span class="hero-heading mb-3">Register</span>
            <div class="w-100">
                <div class="d-flex flex-column mb-4">
                    <div class="coolinput mb-4">
                        <label for="input" class="text">Name</label>
                        <input type="text" placeholder="Enter your name" name="input" class="input">
                    </div>
                    <div class="coolinput mb-4">
                        <label for="input" class="text">Email</label>
                        <input type="email" placeholder="Enter your email" name="input" class="input">
                    </div>
                    <div class="coolinput mb-4">
                        <label for="input" class="text">Password</label>
                        <input type="password" placeholder="Enter your password" name="input" class="input">
                    </div>
                    <button type="submit" class="button button-solid mt-3">Register</button>
                    <span class="link-text">
                        Don’t have an account? <RouterLink to="/login" class="link-pass">Sign in</RouterLink>
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>