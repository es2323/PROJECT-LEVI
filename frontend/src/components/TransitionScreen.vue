<template>
  <div class="transition-container">
    <div class="icon-wrapper">
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
    </div>
    <h1 class="title">Analysis Complete</h1>
    <p class="subtitle">
      Levi has successfully analyzed your CV
      <br>
      Please answer a few short questions to better tailor your roadmap
    </p>
    <button @click="handleContinue" class="cta-button">Continue</button>
  </div>
</template>

<script setup>
const emit = defineEmits(['continue-to-questionnaire']);

function handleContinue() {
  emit('continue-to-questionnaire');
}
</script>

<style scoped>
.transition-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 100%;
  
}
.icon-wrapper {
  color: var(--accent-color);
  border: 2px solid var(--accent-color);
  border-radius: 50%;
  padding: 1rem;
  margin-bottom: 2rem;
}
.title {
  font-size: 3.5rem;
  font-weight: 600;
  margin: 0;
}
.subtitle {
  font-size: 1.4rem;
  opacity: 0.8;
  margin: 1rem 0 2rem 0;
  max-width: 700px;
  line-height: 1.6;
}
.cta-button {
    font-size: 1rem;
  padding: 1rem 2rem;
  background-color: var(--accent-color);
  color: var(--background-color);
  font-weight: 700;
  text-decoration: none;
  border-radius: 60px;
  transition: transform 0.2s;
  cursor: pointer; 
  
}
.cta-button:hover {
  transform: scale(1.05);
}
</style>