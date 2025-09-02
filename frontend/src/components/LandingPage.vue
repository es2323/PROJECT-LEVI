<!-- frontend/src/components/LandingPage.vue -->
<template>
  <div class="landing-container">
    <h1 class="main-title">
      <Typewriter 
        text="Welcome to Project Levi"
        speed= 80
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

function redirectToGoogleLogin() {
  // 1. Get your Client ID from the environment variables
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  // 2. This is the backend endpoint Google will redirect the user back to
  const redirectUri = "http://127.0.0.1:8000/api/auth/google/callback";
  
  // 3. These are the permissions you're asking for
  const scope = "openid profile email";
  
  // 4. Construct the full Google OAuth URL
  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=${scope}&access_type=offline&prompt=consent`;

  // 5. Redirect the user to that URL
  window.location.href = authUrl;
}
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
  border-radius: 60px;
  transition: transform 0.2s;
}

.cta-button:hover {
  transform: scale(1.05);
}
</style>