<script setup>
// Import your new component
import Questionnaire from './components/Questionnaire.vue';
</script>

<template>
  <main>
    <router-view />
  </main>
</template>

<style scoped>
main {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding-top: 2rem;
}
</style>