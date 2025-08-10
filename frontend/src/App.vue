<template>
  <div>
    <!-- Section 1: Landing Page -->
    <section id="landing">
      <LandingPage />
    </section>

    <!-- Section 2: CV Uploader -->
    <section id="upload">
      <CVUploader @cv-uploaded="showQuestionnaire" />
    </section>

    <!-- Section 3: Questionnaire (hidden until CV is uploaded) -->
    <section v-if="isQuestionnaireVisible" id="questionnaire">
      <Questionnaire :cv-skills="userCvSkills" />
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import LandingPage from './components/LandingPage.vue';
import CVUploader from './components/CVUploader.vue';
import Questionnaire from './components/Questionnaire.vue';

const isQuestionnaireVisible = ref(false);

// 3. The variable is created here
const userCvSkills = ref([]);

// 4. The function receives the skills and updates the variable
function showQuestionnaire(skillsFromEmit) {
  userCvSkills.value = skillsFromEmit;
  isQuestionnaireVisible.value = true;
  console.log("Skills have been successfully stored in App.vue:", userCvSkills.value);

  // This smoothly scrolls the user to the questionnaire after it appears
  setTimeout(() => {
    document.getElementById('questionnaire')?.scrollIntoView({ behavior: 'smooth' });
  }, 100);
}
</script>

<style scoped>
section {
  min-height: 100vh; /* Ensures each section is full-height */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}
</style>