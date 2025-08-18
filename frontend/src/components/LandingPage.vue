<!-- frontend/src/components/LandingPage.vue -->
<template>
  <div class="landing-container">
    <h1 class="main-title">
      <Typewriter 
        text="Welcome to Project Levi"
        speed="80"
      />
    </h1>
    <p class="subtitle">
        <Typewriter
        text='Upload your CV    <br>
        Answer a few questions    <br>
        Let Levi build a roadmap for you'
        speed="80"
        :delay="2000"
      />
    </p>
    <a href="#upload" class="cta-button">Get Started</a>
  </div>
</template>

<script setup>
import Typewriter from './Typewriter.vue';
</script>

<style scoped>
.landing-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* Makes the section take up the full screen height */
  text-align: center;
  padding: 2rem;
}

.main-title {
  font-size: 6rem;
  font-weight: 700;
  color: var(--accent-color);
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 2rem;
  max-width: 900px;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-button {
  padding: 1rem 2rem;
  background-color: var(--accent-color);
  color: var(--background-color);
  font-weight: 700;
  text-decoration: none;
  border-radius: 40px;
  transition: transform 0.2s;
}

.cta-button:hover {
  transform: scale(1.05);
}
</style>