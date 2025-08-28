<template>
  <div>
    <div class="debug-view">
      Current View: {{ currentView }}
    </div>
    <NavBar />

    <!-- Section 1: Landing Page (Always visible) -->
    <section id="landing">
      <LandingPage />
    </section>

    <!-- Section 2: CV Uploader (Always visible) -->
    <section id="upload">
      <CVUploader @cv-uploaded="handleCvUploaded" />
    </section>
    <!-- The following sections will appear here as the user progresses -->
    <Transition name="fade" mode="out-in">
      <div :key="currentView">
        <section v-if="currentView === 'transition'" id="transition">
          <TransitionScreen @continue-to-questionnaire="handleContinue" />
        </section>

        <section v-else-if="currentView === 'questionnaire'" id="questionnaire">
          <Questionnaire 
            :cv-skills="userCvSkills" 
            @questionnaire-complete="handleQuestionnaireComplete" 
          />
        </section>
        
        <section v-else-if="currentView === 'results'" id="roadmap">
          <RoadmapView :roadmap-data="roadmapData" />
        </section>
      </div>
    </Transition>
    
    <!-- The full-screen loader is separate so it can cover everything -->
    <Transition name="fade">
      <RoadmapLoader v-if="currentView === 'loading'" />
    </Transition>
    <!-- You can add your static About and Contact sections at the end -->
    <section id="about">
      <h2>About LEVI</h2>
      <p>...</p>
    </section>
    <section id="contact">
      <h2>Contact Us</h2>
      <p>...</p>
    </section>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import NavBar from './components/NavBar.vue';
import LandingPage from './components/LandingPage.vue';
import CVUploader from './components/CVUploader.vue';
import TransitionScreen from './components/TransitionScreen.vue';
import Questionnaire from './components/Questionnaire.vue';
import RoadmapLoader from './components/RoadmapLoader.vue';
import RoadmapView from './components/RoadmapView.vue';

// The state manager for the entire application flow
const currentView = ref(null);
const userCvSkills = ref([]);
const roadmapData = ref(null);

function handleCvUploaded(skills) {
  userCvSkills.value = skills;
  currentView.value = 'transition';
  nextTick(() => {
    document.getElementById('transition')?.scrollIntoView({ behavior: 'smooth' });
  });}

function handleContinue() {
  currentView.value = 'questionnaire';
  nextTick(() => {
    document.getElementById('questionnaire')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });}

// ADDED: This function was missing. It triggers the loading screen.
async function handleQuestionnaireComplete(questionnaireAnswers) {
  currentView.value = 'loading';
  try {
    // --- This is where you will make the REAL final API call ---
    console.log("App.vue received the final data, now calling backend to generate roadmap...");
    // const response = await axios.post('/api/generate-roadmap', { ... });
    // roadmapData.value = response.data;
    
    await new Promise(resolve => setTimeout(resolve, 8000)); // Simulate AI process
    
    currentView.value = 'results';
    nextTick(() => {
      document.getElementById('roadmap')?.scrollIntoView({ behavior: 'smooth' });
    });
  } catch (error) {
    console.error("Failed to generate roadmap:", error);
    // You could add an error view here: currentView.value = 'error';
  }
}
</script>

<style scoped>
section {
  min-height: 100vh;
  padding: 6rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.debug-view {
  position: fixed;
  top: 5rem;
  left: 1rem;
  background-color: rgba(0,0,0,0.7);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  z-index: 9999;
  font-family: monospace;
}
</style>