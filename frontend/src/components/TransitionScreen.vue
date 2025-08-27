<template>
  <div class="transition-container">
    <div class="icon-wrapper">
      <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
        <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
        <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
      </svg>
    </div>
    <h1 class="title">Analysis Complete</h1>
    <p class="subtitle">
      Levi has successfully analysed your CV
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
.title {
  font-size: 3rem;
  font-weight: 700;
  margin: 0;
  margin-top: 2rem;
}
.subtitle {
  font-size: 1.5rem;
  opacity: 0.8;
  margin: 1rem 0 2rem 0;
  max-width: 600px;
  line-height: 1.6;
}
.cta-button {
  font-size: 1.1rem;
  padding: 0.75rem 2rem;
  background-color: var(--accent-color);
  color: var(--background-color);
  font-weight: 700;
  text-decoration: none;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}
.cta-button:hover {
  transform: scale(1.05);
}

/* --- Checkmark Animation Styles --- */
.checkmark {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: block;
  stroke-width: 3;
  stroke: var(--accent-color);
  stroke-miterlimit: 10;
  box-shadow: inset 0px 0px 0px var(--accent-color);
  animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
}

.checkmark-circle {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 3;
  stroke-miterlimit: 10;
  stroke: var(--accent-color);
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark-check {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
    stroke: var(--background-color);

}

@keyframes stroke {
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes scale {
  0%, 100% {
    transform: none;
  }
  50% {
    transform: scale3d(1.1, 1.1, 1);
  }
}

@keyframes fill {
  100% {
    box-shadow: inset 0px 0px 0px 40px var(--accent-color);
  }
}
</style>