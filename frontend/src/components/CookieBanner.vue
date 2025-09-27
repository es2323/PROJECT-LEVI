<template>
  <Transition name="slide-up">
    <div v-if="!hasAcceptedCookies" class="cookie-banner">
      <div class="banner-content">
        <p class="banner-text">
          Levi uses essential cookies to manage your session and improve your experience. 
          Find out more on our <a href="#">Privacy Policy</a>.
        </p>
        <button @click="acceptCookies" class="accept-button">Accept</button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const hasAcceptedCookies = ref(true); // Start as true to hide it initially

// This function runs when the user clicks "Accept"
function acceptCookies() {
  hasAcceptedCookies.value = true;
  // Save the user's choice in the browser's storage
  localStorage.setItem('levi_cookies_accepted', 'true');
}

// onMounted runs when the component first loads
onMounted(() => {
  // Check if the user has already accepted cookies on a previous visit
  if (!localStorage.getItem('levi_cookies_accepted')) {
    hasAcceptedCookies.value = false; // If not, show the banner
  }
});
</script>

<style scoped>
.cookie-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 30%;
  z-index: 1000;
  padding: 1rem;
}
.banner-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;

  /* The Glass Effect */
  background: rgba(251, 251, 251, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(251, 251, 251, 0.15);
  border-radius: 12px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}
.banner-text {
  margin: 0;
  font-size: 0.85rem;
  opacity: 0.9;
  line-height: 1.5;
}
.banner-text a {
  color: var(--accent-color);
  font-weight: 700;
  text-decoration: underline;
}
.accept-button {
  background-color: var(--accent-color);
  color: var(--background-color);
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: opacity 0.2s;
}
.accept-button:hover {
  opacity: 0.9;
}
/* Animation for the banner sliding up */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.5s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(200px);
}
</style>