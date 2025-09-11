<template>
  <nav class="navbar">
    <div class="nav-left">
      <div class="nav-logo">
        <a href="#landing">
          <img src="/nav-logo.png" alt="Project Levi Logo" class="logo-img">
        </a>
      </div>
      <div class="nav-links"> 
      <a href="#demo">See Levi in Action</a> 
      <a href="#upload">The Proccess</a>
      <a href="#about">Why Levi?</a>
      <a href="#faqs">Help Centre</a>
      </div>
      </div>
    <div class="nav-cta">
      <div v-if="isAuthenticated" class="user-info">
        <span>Welcome, {{ user.name.split(' ')[0] }}</span>
        <button @click="logout" class="logout-button">Logout</button>
      </div>
      <a v-else href="#upload" class="cta-button">Get Started for Free</a>
    </div>
  </nav>
</template>

<script setup>
import { useAuth } from '../composables/useAuth';

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
const { isAuthenticated, user, logout } = useAuth();
</script>

<style scoped>
.navbar {
  /* Positioning */
  position: sticky;
  top: 0;
  width: 100%;
  z-index: 100;

  /* Layout */
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 14rem;  
  /* Styling */
  background-color: rgba(251, 251, 251, 0.05);
  border-bottom: 0.5px solid var(--accent-color);
  
    /* The blur effect */
  backdrop-filter: blur(7px);
  -webkit-backdrop-filter: blur(10px);
  
  /* A subtle border to define the edge of the glass */
  border: 1px solid rgba(251, 251, 251, 0.1);
  
  /* A slightly larger radius looks better with glass */
  border-radius: 0px; 
  
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 2rem; /* Adds space between the logo and the links */
}

.nav-links a {
  color: var(--text-color);
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  padding: 0.8rem;
  transition: color 0.2s;
  opacity: 0.8;

}

.nav-links a:hover {
  color: var(--accent-color);
}

.nav-links {
  display: flex;
  gap: 0.8rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logout-button {
  background-color: transparent;
  color: var(--text-color);
  border: 2px solid var(--text-color);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.8rem;
  cursor: pointer;
  opacity: 0.8;
}
.logout-button:hover {
  opacity: 1;
}

.cta-button {
  background-color: var(--text-color);
  color: var(--background-color);
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 700;
  text-decoration: none;
}
.cta-button:hover {
  opacity: 1;
}
.logo-img {
  height: 50px; /* Adjust this value to make the logo bigger or smaller */
  width: 55px;
  display: block; /* Helps prevent extra space below the image */
}
</style>