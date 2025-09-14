<template>
  <div class="why-levi-container">
    <h2 class="section-title">Why LEVI?</h2>
    <div class="features-grid">
      
      <div class="feature-item">
        <div class="feature-card">
            <TangledLines />
        </div>
        <div class="description">
          <h3>The Problem We Solve</h3>
          <p>Navigating the tech job market as a student is confusing. We built Levi to bring clarity to your career path.</p>
        </div>
      </div>

      <div class="feature-item">
        <div class="feature-card">
          <NeuralAnimation />
        </div>
        <div class="description">
          <h3>Your AI-Powered Solution</h3>
          <p>Levi analyzes your unique profile against a live job market to create a personalised, step-by-step learning plan in the form of a roadmap.</p>
        </div>
      </div>

      <div class="feature-item">
        <div class="feature-card"></div>
        <div class="description">
          <h3>From Students, For Students</h3>
          <p>We're final-year undergrads who understand the journey. We've built you the tool we wish we had.</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import NeuralAnimation from './NeuralAnimation.vue';
import TangledLines from './TangledLines.vue';
</script>

<style scoped>
.why-levi-container {
  width: 100%;
  max-width: 1100px;
  text-align: center;
  padding: 4rem 2rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 3rem;
}

/* This is the new main container for the grid */
.features-grid {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

/* Each item now contains one card and its description */
.feature-item {
  width: 320px; /* Control the width of the entire column here */
  display: flex;
  flex-direction: column;
  gap: 1.5rem; /* Space between card and text */
}

.feature-card {
  width: 100%; /* Card now fills its container */
  height: 260px;
  
  /* The Glass Effect */
  background: rgba(251, 251, 251, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(251, 251, 251, 0.1);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

.description {
  /* No width needed, it will match the item's width */
  text-align: center; /* Center all text inside */
}

.description h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--accent-color);
  margin-bottom: 0.5rem;
}

.description p {
  opacity: 0.8;
  line-height: 1.6;
}
</style>