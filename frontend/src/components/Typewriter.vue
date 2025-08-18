<template>
  <span class="typewriter-text" v-html="displayedText"></span>
  <span class="cursor" :class="{ 'is-blinking': isBlinking }">|</span>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// --- Props ---
// These are the "settings" you can pass to the component.
const props = defineProps({
  // The full text you want to be typed out
  text: {
    type: String,
    required: true,
  },
  // How fast to type in milliseconds
  speed: {
    type: Number,
    default: 1000, // 100ms per character
  },
  // How long to wait before starting in milliseconds
  delay: {
    type: Number,
    default: 0,
  }
});

// --- Reactive State ---
const displayedText = ref('');
const isBlinking = ref(false);

// --- Logic ---
// onMounted is a Vue hook that runs once the component has been added to the page.
onMounted(() => {
  // Wait for the initial delay before starting
  setTimeout(() => {
    isBlinking.value = true;
    let index = 0;
    
    // Set up an interval to add one character at a time
    const typingInterval = setInterval(() => {
      if (index < props.text.length) {
        displayedText.value += props.text.charAt(index);
        index++;
      } else {
        // Stop the interval once the full text is displayed
        clearInterval(typingInterval);
        // You could set isBlinking.value = false; here if you want the cursor to disappear
      }
    }, props.speed);

  }, props.delay);
});
</script>

<style scoped>
/* The blinking animation has been removed from here */
.cursor {
  font-weight: 700;
  color: var(--accent-color);
  opacity: 1;
}

.cursor.is-blinking {
  animation: blink 1s infinite;
}
</style>