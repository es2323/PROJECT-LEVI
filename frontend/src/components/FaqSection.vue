<template>
  <div class="faq-container">
    <h2 class="section-title">Frequently Asked Questions</h2>
    <div class="faq-list">
      <div v-for="(faq, index) in faqs" :key="index" class="faq-item">
        <div class="faq-question" @click="toggleFaq(index)">
          <span>{{ faq.question }}</span>
          <span class="arrow" :class="{ 'open': openFaqIndex === index }">▼</span>
        </div>
        <Transition name="slide-fade">
          <div v-if="openFaqIndex === index" class="faq-answer">
            <p>{{ faq.answer }}</p>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const openFaqIndex = ref(null); // Tracks which FAQ is currently open

const faqs = ref([
  {
    question: "What exactly is Levi and who is it for?",
    answer: "LEVI is an AI-powered career readiness platform designed for university students. It analyses your CV and career goals to create a personalised, step-by-step learning roadmap to help you gain the skills to become job ready. \n\nAt this point in time, Levi is designed for university students and recent graduates in the UK who are looking for direction as they prepare to enter the tech industry."
  },
  {
    question: "How does Levi decide which skills are best for me?",
    answer: "The recommendations are based on a combination of three key data points: the skills extracted from your CV, the answers from your questionnaire which tell us your specific goals and learning style, and real-time data from job market APIs. The AI cross-references what employers are currently looking for with your unique profile to identify the most impactful skills for you to learn."
  },
  {
    question: "How reliable is Levi?",
    answer: "LEVI's analysis is powered by Google's Gemini AI, a state-of-the-art large language model. While the skill extraction from your CV is highly accurate, the roadmap itself is a sophisticated recommendation, not a guarantee. Think of it as a well-informed guide from an expert career coach, designed to give you structure and direction."
  },
  {
    question: "Is my CV data safe?",
    answer: "Yes. We temporarily process the text of your CV to perform the AI analysis. Once the analysis is complete, the only data we keep in your temporary session is the anonymized list of skills that were extracted. The full text of your CV, including all personal information, is immediately discarded."
  },
  {
    question: "Can I save my roadmap and come back to it?",
    answer: "Yes! Simply sign up with your Google account, and come back to your roadmap at any time, you can even track your progress as you complete each skill."
  },
  {
    question: "Is Levi completely free?",
    answer: "Yes, for our current version, all features are completely free to use."
  },
  {
    question: "What is the core mission of LEVI?",
    answer: "Our mission is to solve one of the hardest problems for students: bridging the gap between academic knowledge and real-world job requirements. It's often difficult to know which skills are truly in-demand for a specific role or how to best learn them. LEVI aims to cut through that confusion by using AI to provide a clear, data-driven, and personalized pathway, turning uncertainty into an actionable plan for your career."
  }
]);

function toggleFaq(index) {
  // If the clicked FAQ is already open, close it. Otherwise, open it.
  openFaqIndex.value = openFaqIndex.value === index ? null : index;
}
</script>

<style scoped>
.faq-container {
  width: 100%;
  max-width: 700px;
  text-align: center;
  padding: 4rem 2rem;
}
.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 3rem;
}
.faq-list {
  text-align: left;
}
.faq-item {
  border-bottom: 1px solid rgba(251, 251, 251, 0.1);
}
.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 0;
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: 500;
}
.arrow {
  font-size: 0.8rem;
  transition: transform 0.5s ease;
}
.arrow.open {
  transform: rotate(180deg);
}
.faq-answer {
  overflow: hidden;
  padding: 0 0 1.5rem 0;
  white-space: pre-line; 
}
.faq-answer p {
  margin: 0;
  opacity: 0.8;
  line-height: 1.6;
}
/* Transition for the dropdown effect */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.3s ease;
  max-height: 200px;
}
.slide-fade-enter-from, .slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}
</style>