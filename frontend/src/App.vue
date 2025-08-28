<template>
  <div>
    <NavBar />
    <!-- Section 1: Landing Page -->
    <section id="landing">
      <LandingPage />
    </section>

   <Transition name="fade" mode="out-in">
      <div class="main-content" :key="currentView">
      <section v-if="currentView === 'uploader'" id="upload">
        <CVUploader @cv-uploaded="handleCvUploaded" />
      </section>

      <section v-else-if="currentView === 'transition'" id="transition">
        <TransitionScreen @continue-to-questionnaire="handleContinue" />
      </section>

      <section v-else-if="currentView === 'questionnaire'" id="questionnaire">
        <Questionnaire :cv-skills="userCvSkills" />
      </section>
      </div>
      </Transition>
    <section id="about">
      <h2>About LEVI</h2>
      <p>...</p>
    </section>
    <section id="contact">
      <h2>Contact Us</h2>
      <p>...</p>
    </section>
    <section id="roadmap">
      <RoadmapView />
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import NavBar from './components/NavBar.vue';
import LandingPage from './components/LandingPage.vue';
import CVUploader from './components/CVUploader.vue';
import TransitionScreen from './components/TransitionScreen.vue'; 

import Questionnaire from './components/Questionnaire.vue';
import RoadmapView from './components/RoadmapView.vue'; // <-- Import the new component


const currentView = ref('uploader'); // Possible values: 'uploader', 'transition', 'questionnaire'

// 3. The variable is created here
const userCvSkills = ref([]);

// 3. This function now changes the view to 'transition'
function handleCvUploaded(skills) {
  userCvSkills.value = skills;
  currentView.value = 'transition';
  
  // Scroll to the new section
  setTimeout(() => {
    document.getElementById('transition')?.scrollIntoView({ behavior: 'smooth' });
  }, 100);
}

// 4. This new function changes the view to 'questionnaire'
function handleContinue() {
  currentView.value = 'questionnaire';
  
  // Scroll to the questionnaire
  setTimeout(() => {
    document.getElementById('questionnaire')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 100);
}
</script>

<style scoped>
section {
  min-height: 100vh; /* Ensures each section is full-height */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.7s ease;
}

/* The state an element is in before it enters (hidden) */
.fade-enter-from,
/* The state an element is in after it leaves (hidden) */
.fade-leave-to {
  opacity: 0;
}
</style>