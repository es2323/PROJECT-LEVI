<script setup>
// Importing a child component demonstrates Component-Based Architecture
import CVUploader from './components/CVUploader.vue';
</script>

<template>
  <main>
    <CVUploader />
  </main>
</template>

<style>
/* Global styles can go here if needed */
main {
  font-family: sans-serif;
  padding: 1rem;
}
</style>