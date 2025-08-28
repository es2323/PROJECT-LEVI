<template>
  <div class="loader-wrapper">
    <svg class="loader-svg" viewBox="-55 -55 110 110">
      <path class="loader-path" d="
        M -43.3 -25 L 0 -50 L 43.3 -25 L 43.3 25 L 0 50 L -43.3 25 Z
        M -43.3 -25 L 0 0 L 43.3 -25
        M 0 0 L 0 50
      "/>
    </svg>
    <p v-if="loadingText" class="loading-text">{{ loadingText }}</p>
  </div>
</template>

<script setup>
defineProps({
  loadingText: String,
});
</script>

<style scoped>
.loader-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loader-svg {
  width: 100px;
  height: 100px;
  animation: spin 5s linear infinite; /* Slowed down the spin slightly */
}

.loader-path {
  fill: none;
  stroke: var(--accent-color);
  stroke-width: 2; /* Made the line slightly thinner for a more technical look */
  stroke-linecap: round;
  
  /* CHANGED: Updated the length to match the new cube path */
  stroke-dasharray: 450;
  stroke-dashoffset: 450;
  
  animation: draw 3s ease-in-out infinite; /* Slowed down the draw slightly */
}

.loading-text {
  font-weight: 400;
  font-size: 1.2rem;
  opacity: 0.8;
}

/* Animation for the path drawing itself */
@keyframes draw {
  0% {
    stroke-dashoffset: 450;
  }
  50% {
    stroke-dashoffset: 0;
  }
  100% {
    stroke-dashoffset: -450;
  }
}

/* Animation for the whole shape rotating */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>