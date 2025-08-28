<template>
  <div class="loader-overlay">
    <SvgLoader :loading-text="currentStatus" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import SvgLoader from './SvgLoader.vue';

const currentStatus = ref('');
let statusInterval;

// The messages to cycle through
const statuses = [
  "Analyzing your skills against the job market...",
  "Identifying your key strengths and gaps...",
  "Generating personalized learning steps...",
  "Building your final roadmap..."
];

onMounted(() => {
  let statusIndex = 0;
  currentStatus.value = statuses[statusIndex];

  // Set up an interval to cycle through the messages
  statusInterval = setInterval(() => {
    statusIndex++;
    // Hold on the last message if the process is still running
    if (statusIndex < statuses.length) {
      currentStatus.value = statuses[statusIndex];
    }
  }, 2500); // Change message every 2.5 seconds
});

// Clean up the interval when the component is removed
onUnmounted(() => {
  clearInterval(statusInterval);
});
</script>

<style scoped>
.loader-overlay {
  position: fixed; /* Use fixed to cover the entire viewport */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--background-color); /* Use your main background color */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200; /* Ensure it's on top of everything */
}
</style>