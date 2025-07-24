<template>
  <div class="questionnaire-container">
    <h2>Tell us more about your goals!</h2>
    <p class="subtitle">This will help us build the perfect roadmap for you.</p>
    
    <form @submit.prevent="handleSubmit" class="form-wrapper">
      <div class="form-group">
        <label>Which tech sectors are you most passionate about pursuing?</label>
        <MultiSelectDropdown 
          :options="fieldOptions"
          v-model="formData.techField"
          placeholder="Select a field..."
        />
      </div>

      <div class="form-group">
        <label>What type of roles do you see yourself doing?</label>
        <MultiSelectDropdown 
          :options="roleOptions"
          v-model="formData.roleType"
          placeholder="Select a role..."
        />
      </div>

      <div class="form-group">
        <label>Which of these skills are you most interested in developing?</label>
        <MultiSelectDropdown 
          :options="skillOptions"
          v-model="formData.skillsOfInterest"
          placeholder="Select skills..."
        />
      </div>

      <div class="form-group">
        <label>What industries excite you the most?</label>
        <MultiSelectDropdown 
          :options="industryOptions"
          v-model="formData.industries"
          placeholder="Select industries..."
        />
      </div>
      
      <button type="submit">Generate My Roadmap</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import MultiSelectDropdown from './MultiSelectDropdown.vue';

// Define the options for each dropdown
const fieldOptions = ref([
  { value: 'fintech', label: 'FinTech (Financial Technology) 💰' },
  { value: 'healthtech', label: 'HealthTech (Healthcare Technology) 🩺' },
  { value: 'ai_ml', label: 'AI / Machine Learning 🤖' },
  { value: 'ecommerce', label: 'E-commerce & Retail 🛍️' },
  { value: 'game', label: 'Gaming & Entertainment 🎮' },
  { value: 'edtech', label: 'EdTech (Education Technology) 🎓' },
  { value: 'greentech', label: 'GreenTech & Sustainability 🌍' },
  { value: 'cars', label: 'Automotive & Transportation 🚗' },
  { value: 'gov', label: 'GovTech & Public Sector 🏛️' }
]);

const roleOptions = ref([
  { value: 'startup', label: 'Fast-paced Startup' },
  { value: 'corporate', label: 'Large Corporation' },
  { value: 'mid-size', label: 'Mid-sized Tech Company' },
  { value: 'public-sector', label: 'Public Sector / Government' }
]);

const skillOptions = ref([
  { value: 'js_frameworks', label: 'JavaScript Frameworks (React, Vue)' },
  { value: 'python_data', label: 'Python for Data Science' },
  { value: 'cloud_aws', label: 'Cloud Platforms (AWS)' },
  { value: 'databases', label: 'Databases (SQL, NoSQL)' }
]);

const industryOptions = ref([
  { value: 'fintech', label: 'Finance (FinTech)' },
  { value: 'healthtech', label: 'Healthcare (HealthTech)' },
  { value: 'gaming', label: 'Gaming & Entertainment' },
  { value: 'ecommerce', label: 'E-commerce' }
]);

// Use a single reactive object to hold all form data
const formData = ref({
  techField: [],
  roleType: [],
  skillsOfInterest: [],
  industries: []
});

function handleSubmit() {
  console.log("Final form data:", formData.value);
  // Next step: send this data to the backend
}
</script>

<style scoped>
body { /* This won't apply globally, just for context */
  background-color: #374954;
}

.questionnaire-container {
  width: 500px;
  margin: 0 auto;
  padding: 50px;
  background-color: #374954;
  color: #fff;
  font-family: "Andale Mono", AndaleMono, monospace;
}

.subtitle {
  margin-bottom: 2rem;
  opacity: 0.8;
}

.form-wrapper {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-group {
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.75rem;
}

button {
  background-color: #6BBE92;
  width: 100%;
  border: 0;
  padding: 12px 0;
  margin-top: 1rem;
  text-align: center;
  color: #fff;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
}
</style>