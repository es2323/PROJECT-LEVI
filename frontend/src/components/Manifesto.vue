<template>
  <Transition name="fade">
    <div class="modal-overlay" @click.self="emit('close')">
      <div class="modal-content">
        <button @click="emit('close')" class="close-button">×</button>
        <h2 class="section-title">Our Manifesto</h2>
        <div class="manifesto-text">
You learn to code.
They ask for a career.

You follow the tutorials.
You guess at the skills.
You hope you are ready.

Some call AI the answer.
We call it the compass.

A tool not to automate your future,
but to amplify your judgment. 

LEVI sees your experience.
It hears your ambition.
It maps the market.
And draws your unique path from here to there.

The future won't reward scattered effort.
It will reward intentional learning.

Stop guessing.
Start building.
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineEmits(['close']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  position: relative;
  width: 100%;
  max-width: 800px;
  padding: 3rem;
  
  /* The Glass Effect */
  background: var(--background-color);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(251, 251, 251, 0.1);
  border-radius: 16px;
}
.close-button {
  position: absolute;
  top: 1rem;
  right: 1.5rem;
  background: none;
  border: none;
  font-size: 2rem;
  color: var(--text-color);
  opacity: 0.5;
  cursor: pointer;
}
.section-title {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: var(--accent-color);
}
.manifesto-text {
  font-size: 1.1rem;
  line-height: 1.8;
  opacity: 0.9;
}
/* Fade animation for the modal */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>