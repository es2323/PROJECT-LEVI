<template>
  <div>
    <div class="debug-view">
      Current View: {{ currentView }}
    </div>
    <div class="debug-controls">
      <button @click="login">Simulate Login</button>
    </div>
    <NavBar />

    <!-- Section 1: Landing Page (Always visible) -->
    <section id="landing">
      <LandingPage />
    </section>

    <!--TreeMap-->
    <section id="demo">
      <treeMap />
    </section>

    <!-- Section 2: CV Uploader (Always visible) -->
    <section id="upload">
      <CVUploader 
        @cv-uploaded="handleCvUploaded" 
        @skip-to-roadmap="handleSkipToRoadmap" 
      />
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
      <WhyLevi />
    </section>
    <section id="help">
      <FaqSection />
    </section>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue';
import NavBar from './components/NavBar.vue';
import LandingPage from './components/LandingPage.vue';
import CVUploader from './components/CVUploader.vue';
import TransitionScreen from './components/TransitionScreen.vue';
import Questionnaire from './components/Questionnaire.vue';
import RoadmapLoader from './components/RoadmapLoader.vue';
import RoadmapView from './components/RoadmapView.vue';
import axios from 'axios'; // Import axios
import { mockData } from './data/mockRoadmapData.js'
import { useAuth } from './composables/useAuth';
import treeMap from './components/treeMap.vue';
import WhyLevi from './components/WhyLevi.vue';
import FaqSection from './components/FaqSection.vue';




// The state manager for the entire application flow
const currentView = ref(null);
const userCvSkills = ref([]);
const roadmapData = ref(null);
const { login } = useAuth();

onMounted(() => {
  // This command instantly scrolls the page to the top-left corner.
  window.scrollTo(0, 150);
});

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
    await new Promise(resolve => setTimeout(resolve, 8000));
    roadmapData.value = mockData;
    currentView.value = 'results';
    nextTick(() => {
      document.getElementById('roadmap')?.scrollIntoView({ behavior: 'smooth' });
    });
  } catch (error) {
    console.error("Failed to generate roadmap:", error);
  }
}
function handleSkipToRoadmap() {
  console.log("Skipping directly to roadmap with mock data.");
  roadmapData.value = mockData; // Load the mock data
  currentView.value = 'results'; // Change the view

  nextTick(() => {
    document.getElementById('roadmap')?.scrollIntoView({ behavior: 'smooth' });
  });
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
  top: 12rem;
  left: 1rem;
  background-color: rgba(0,0,0,0.7);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  z-index: 9999;
  font-family: monospace;
}

.debug-controls {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 9999;
}
</style>