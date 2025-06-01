<template>
    <div class="signin-wrapper">
        <div class="signin-card ">
            <span class="hero-heading mb-3">log in</span>
            <div class="w-100">
                <div class="d-flex flex-column mb-4">
                    <div class="coolinput mb-4">
                        <label for="input" class="text">Email</label>
                        <input type="email" placeholder="Enter your email" name="input" class="input">
                    </div><!-- From Uiverse.io by kamehame-ha -->
                    <div class="coolinput mb-4">
                        <label for="input" class="text">Password</label>
                        <input type="password" placeholder="Enter your password" name="input" class="input">
                    </div>
                    <a href="#" class="link-pass">Forgot Password?</a>
                    <button type="submit" class="button button-solid mt-3">Sign in</button>
                    <span class="link-text">
                        Don’t have an account? <RouterLink to="/register" class="link-pass">Register</RouterLink>
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>