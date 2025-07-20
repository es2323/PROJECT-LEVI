<template>
  <div class="questionnaire-container">
    <h2>Just a few quick questions...</h2>
    <p class="subtitle">Your answers will help us create a truly personalised roadmap for you.</p>

    <form @submit.prevent="handleSubmit">
    <fieldset class="form-group">
        <legend>What tech field are you most passionate about pursuing?</legend>
        <div class="options-group">
        <label><input type="radio" name="techField" value="frontend" v-model="techField"> Frontend</label>
        <label><input type="radio" name="techField" value="backend" v-model="techField"> Backend</label>
        <label><input type="radio" name="techField" value="ai_ml" v-model="techField"> AI / Machine Learning</label>
        <label><input type="radio" name="techField" value="devops" v-model="techField"> DevOps / Cloud</label>
        </div>
    </fieldset>

    <fieldset class="form-group">
        <legend>How do you learn best?</legend>
        <div class="options-group">
        <label><input type="radio" name="learningStyle" value="visual" v-model="learningStyle"> Visual (Videos)</label>
        <label><input type="radio" name="learningStyle" value="practical" v-model="learningStyle"> Practical (Projects)</label>
        <label><input type="radio" name="learningStyle" value="reading" v-model="learningStyle"> Reading (Docs)</label>
        </div>
    </fieldset>

    <fieldset class="form-group">
        <legend>What type of company environment are you most drawn to?</legend>
        <div class="options-group">
        <label><input type="radio" name="companyType" value="startup" v-model="companyType"> Fast-paced Startup</label>
        <label><input type="radio" name="companyType" value="corporate" v-model="companyType"> Large Corporation</label>
        <label><input type="radio" name="companyType" value="mid-size" v-model="companyType"> Mid-sized Company</label>
        </div>
    </fieldset>

    <fieldset class="form-group">
        <legend>How confident do you feel in your primary programming language?</legend>
        <div class="options-group rating">
        <label>1 <input type="radio" name="confidence" value="1" v-model="confidence"></label>
        <label>2 <input type="radio" name="confidence" value="2" v-model="confidence"></label>
        <label>3 <input type="radio" name="confidence" value="3" v-model="confidence"></label>
        <label>4 <input type="radio" name="confidence" value="4" v-model="confidence"></label>
        <label>5 <input type="radio" name="confidence" value="5" v-model="confidence"></label>
        </div>
    </fieldset>

    <fieldset class="form-group">
        <legend>Which of these best describes what you enjoy doing?</legend>
        <div class="options-group">
        <label><input type="radio" name="enjoyment" value="ui" v-model="enjoyment"> Building user interfaces</label>
        <label><input type="radio" name="enjoyment" value="architecture" v-model="enjoyment"> Designing server architectures</label>
        <label><input type="radio" name="enjoyment" value="data" v-model="enjoyment"> Analysing data for insights</label>
        </div>
    </fieldset>

    <button type="submit">Get My Roadmap</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Create a reactive variable for each question's answer
const techField = ref(null);
const learningStyle = ref(null);
const companyType = ref(null);
const confidence = ref(null);
const enjoyment = ref(null);

function handleSubmit() {
  // Log the collected data to see that it's working
  const formData = {
    techField: techField.value,
    learningStyle: learningStyle.value,
    companyType: companyType.value,
    confidence: confidence.value,
    enjoyment: enjoyment.value,
  };
  console.log("Questionnaire Data:", formData);
  // The logic to send this data to the backend will go here next
}
</script>

<style scoped>
.questionnaire-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background-color: #fff;
  font-family: sans-serif;
}

.subtitle {
  color: #4a5568;
  margin-bottom: 2rem;
}

.form-group {
  border: none;
  padding: 0;
  margin: 0 0 2rem 0;
  text-align: left;
}

legend {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  padding: 0;
  width: 100%;
}

.options-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.options-group.rating {
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.options-group.rating label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.options-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
}

input[type="radio"] {
  width: 1rem;
  height: 1rem;
}

button {
  width: 100%;
  padding: 0.8rem;
  background-color: #38a169; /* Green color */
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1rem;
}
</style>