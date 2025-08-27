<template>
  <div>
    <NavBar />
    <!-- Section 1: Landing Page -->
      <section v-if="currentView === 'landing'" id="landing">
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
        <Questionnaire :cv-skills="userCvSkills" @questionnaire-complete="handleQuestionnaireComplete" />
      </section>
      
      <section v-else-if="currentView === 'results'" id="roadmap">
        <RoadmapView :roadmap-data="roadmapData" />
      </section>
      </div>
    <Transition name="fade">
      <RoadmapLoader v-if="currentView === 'loading'" />
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
import RoadmapLoader from './components/RoadmapLoader.vue'; // 1. Import new loader


import Questionnaire from './components/Questionnaire.vue';
import RoadmapView from './components/RoadmapView.vue'; // <-- Import the new component


const currentView = ref('landing'); // Possible values: 'uploader', 'transition', 'questionnaire'

// 3. The variable is created here
const userCvSkills = ref([]);
const roadmapData = ref(null); // To store the final roadmap


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
  setTimeout(() => { document.getElementById('questionnaire')?.scrollIntoView({ behavior: 'smooth' }); }, 100);
}

// 3. This new function handles the final step
async function handleQuestionnaireComplete(questionnaireAnswers) {
  // Switch to the full-screen loading view
  currentView.value = 'loading';

  // --- This is where you will make the REAL final API call ---
  try {
    // const response = await axios.post('/api/generate-roadmap', { ... });
    // roadmapData.value = response.data;
    
    // SIMULATION FOR NOW
    await new Promise(resolve => setTimeout(resolve, 8000)); // Simulate a long AI process
    // roadmapData.value = { ... MOCK DATA ... }; // Use mock data for testing

    // Switch to the results view on success
    currentView.value = 'results';
    setTimeout(() => { document.getElementById('roadmap')?.scrollIntoView({ behavior: 'smooth' }); }, 100);

  } catch (error) {
    console.error("Failed to generate roadmap:", error);
    // You could add an error view: currentView.value = 'error';
  }
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