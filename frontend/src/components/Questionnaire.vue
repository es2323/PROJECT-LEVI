<template>
  <div class="questionnaire-container">
        <h2 class="main-title">
      <Typewriter 
        text="Tell us more about your goals!" 
        :speed="50"
      />
    </h2>
    <p class="subtitle">This will help Levi build the perfect roadmap for you.</p>
    
    <form @submit.prevent="handleSubmit" class="form-wrapper">
      <div class="form-group">
        <label for="sector-select">What tech sector(s) are you most passionate about pursuing?</label>
        <select id="sector-select" v-model="formData.sector" class="custom-select">
          <option disabled value="">Please select one</option>
          <option v-for="option in sectorOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <div v-if="formData.sector" class="form-group">
        <label>What type of role(s) do you see yourself doing? (Select up to 3)</label>
        <div v-for="role in dynamicRoleOptions" :key="role.value" class="checkbox-group">
          <label>
            <input 
              type="checkbox" 
              :value="role.value" 
              v-model="formData.roles"
              :disabled="formData.roles.length >= 3 && !formData.roles.includes(role.value)"
            >
            {{ role.label }}
          </label>
        </div>

        <div class="other-group">
          <div class="checkbox-group">
            <label>
              <input type="checkbox" v-model="isRoleOtherSelected">
              Other
            </label>
          </div>
          <input 
            v-if="isRoleOtherSelected"
            type="text" 
            placeholder="Please specify a custom role..." 
            v-model="formData.roleOther"
            class="other-input"
          >
        </div>
      </div>

      <fieldset class="form-group">
        <legend>Looking ahead 5 years, what career level do you aspire to reach?</legend>
        <div class="options-group">
          <label><input type="radio" value="expert" v-model="formData.ambition"> Senior Technical Expert</label>
          <label><input type="radio" value="leadership" v-model="formData.ambition"> Team Leadership</label>
          <label><input type="radio" value="product" v-model="formData.ambition"> Product-focused Role</label>
          <label><input type="radio" value="unsure" v-model="formData.ambition"> Not sure yet</label>
        </div>
      </fieldset>
      
      <fieldset class="form-group">
        <legend>Which type of technical challenge are you most excited to solve?</legend>
        <div class="options-group">
          <label><input type="checkbox" value="ui" v-model="formData.passion"> Building user interfaces</label>
          <label><input type="checkbox" value="backend" v-model="formData.passion"> Designing backend systems</label>
          <label><input type="checkbox" value="data" v-model="formData.passion"> Finding insights in data</label>
          <label><input type="checkbox" value="automation" v-model="formData.passion"> Automating infrastructure</label>
        </div>
      </fieldset>

      <fieldset class="form-group">
        <legend>Thinking about your top technical skill, how would you rate your ability?</legend>
        <div class="options-group">
          <label><input type="radio" value="foundational" v-model="formData.confidence"> Foundational (Used in tutorials)</label>
          <label><input type="radio" value="intermediate" v-model="formData.confidence"> Intermediate (Built a personal project)</label>
          <label><input type="radio" value="advanced" v-model="formData.confidence"> Advanced (Ready for production code)</label>
        </div>
      </fieldset>

      <fieldset class="form-group">
        <legend>What is the best way you learn?</legend>
        <div class="options-group">
          <label><input type="checkbox" value="visual" v-model="formData.learningStyle"> Visual (videos)</label>
          <label><input type="checkbox" value="auditory" v-model="formData.learningStyle"> Auditory (lectures)</label>
          <label><input type="checkbox" value="reading" v-model="formData.learningStyle"> Reading/Writing (docs)</label>
          <label><input type="checkbox" value="kinaesthetic" v-model="formData.learningStyle"> Kinaesthetic (projects)</label>
        </div>
      </fieldset>

      <fieldset class="form-group">
        <legend>When learning, what are you most drawn to?</legend>
        <div class="options-group">
          <label><input type="radio" value="cutting-edge" v-model="formData.techPreference"> The latest, cutting-edge tech</label>
          <label><input type="radio" value="stable" v-model="formData.techPreference"> Widely-adopted, stable tech</label>
          <label><input type="radio" value="mix" v-model="formData.techPreference"> A mix of both</label>
        </div>
      </fieldset>

      <fieldset class="form-group">
        <legend>What kind of work pace are you most comfortable with?</legend>
        <div class="options-group">
          <label><input type="radio" value="fast" v-model="formData.workPace"> Dynamic & Fast-Paced (learning many things)</label>
          <label><input type="radio" value="focused" v-model="formData.workPace"> Structured & Deep-Focused (mastering one thing)</label>
        </div>
      </fieldset>
      
      <button type="submit">Generate My Roadmap</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import Typewriter from './Typewriter.vue';
const props = defineProps({
  cvSkills: Array
});
// Define the options for each dropdown
const sectorOptions = ref([
  { value: 'fintech', label: 'FinTech (Financial Technology) 💰' },
  { value: 'healthtech', label: 'HealthTech (Healthcare Technology) 🩺' },
  { value: 'ai_ml', label: 'AI / Machine Learning 🤖' },
  { value: 'ecommerce', label: 'E-commerce & Retail 🛍️' },
  { value: 'game', label: 'Gaming & Entertainment 🎮' },
  { value: 'edtech', label: 'EdTech (Education Technology) 🎓' },
  { value: 'greentech', label: 'GreenTech & Sustainability 🌍' },
  { value: 'cars', label: 'Automotive & Transportation 🚗' },
  { value: 'gov', label: 'GovTech & Public Sector 🏛️' },
  { value: 'idk', label: "I'm not sure yet, give me general tech roles. 🤔" }// ADDED IDK option
]);

const generalRoles = [
  { value: 'swe', label: 'Graduate Software Engineer' },
  { value: 'backend', label: 'Backend Developer' },
  { value: 'frontend', label: 'Frontend Developer' },
  { value: 'cloud', label: 'Cloud / DevOps Engineer' },
  { value: 'data_analyst', label: 'Data Analyst' }
];
// 1. THE DATA MAP: Maps sectors to their specific roles
const rolesBySector = {
  fintech: [
    { value: 'quant_dev', label: 'Quantitative Developer' },
    { value: 'backend_payments', label: 'Backend Engineer (Payments)' },
    { value: 'cybersec_finance', label: 'Cybersecurity Analyst (Finance)' },
    { value: 'data_fraud', label: 'Data Scientist (Fraud Detection)' },
    { value: 'fullstack_trading', label: 'Full-Stack Developer (Trading Platforms)' }
  ],
  healthtech: [
    { value: 'ml_imaging', label: 'ML Engineer (Medical Imaging)' },
    { value: 'fullstack_emr', label: 'Full-Stack Developer (EHR Systems)' },
    { value: 'data_privacy_eng', label: 'Data Privacy Engineer' },
    { value: 'backend_patient_api', label: 'Backend Engineer (Patient Data APIs)' },
    { value: 'mobile_health', label: 'Mobile Health App Developer' }
  ],
  ai_ml: [
    { value: 'ml_engineer', label: 'Machine Learning Engineer' },
    { value: 'research_scientist', label: 'Research Scientist' },
    { value: 'nlp_engineer', label: 'NLP Engineer' },
    { value: 'computer_vision_eng', label: 'Computer Vision Engineer' },
    { value: 'ai_product_manager', label: 'AI Product Manager' }
  ],
  ecommerce: [
    { value: 'frontend_storefront', label: 'Frontend Developer (Storefronts)' },
    { value: 'backend_orders', label: 'Backend Engineer (Order Management)' },
    { value: 'data_analyst_sales', label: 'Data Analyst (Sales Trends)' },
    { value: 'sre_ecommerce', label: 'Site Reliability Engineer (High Traffic)' },
    { value: 'search_recommendation', label: 'Search & Recommendations Engineer' }
  ],
  game: [
    { value: 'gameplay_eng', label: 'Gameplay Engineer' },
    { value: 'graphics_eng', label: 'Graphics Programmer' },
    { value: 'game_engine_tools', label: 'Game Engine Tools Developer' },
    { value: 'backend_online', label: 'Backend Engineer (Online Services)' },
    { value: 'qa_automation_game', label: 'QA Automation Engineer (Gaming)' }
  ],
  edtech: [
    { value: 'fullstack_lms', label: 'Full-Stack Developer (LMS)' },
    { value: 'mobile_learning', label: 'Mobile Learning Developer' },
    { value: 'instructional_designer_tech', label: 'Instructional Designer (Technical)' },
    { value: 'backend_student_data', label: 'Backend Engineer (Student Data)' },
    { value: 'frontend_interactive', label: 'Frontend Developer (Interactive Content)' }
  ],
  greentech: [
    { value: 'data_scientist_climate', label: 'Data Scientist (Climate Modeling)' },
    { value: 'iot_smart_grid', label: 'IoT Engineer (Smart Grids)' },
    { value: 'backend_energy', label: 'Backend Engineer (Energy Trading)' },
    { value: 'fullstack_carbon', label: 'Full-Stack Developer (Carbon Tracking)' },
    { value: 'gis_developer_green', label: 'GIS Developer (Renewable Energy)' }
  ],
  cars: [
    { value: 'embedded_systems_auto', label: 'Embedded Systems Engineer' },
    { value: 'computer_vision_adas', label: 'Computer Vision Engineer (ADAS)' },
    { value: 'backend_fleet', label: 'Backend Engineer (Fleet Management)' },
    { value: 'mobile_ridesharing', label: 'Mobile App Developer (Ride-Sharing)' },
    { value: 'robotics_auto', label: 'Robotics Software Engineer' }
  ],
  gov: [
    { value: 'fullstack_citizen', label: 'Full-Stack Developer (Citizen Services)' },
    { value: 'cybersec_gov', label: 'Cybersecurity Analyst (Public Sector)' },
    { value: 'data_analyst_policy', label: 'Data Analyst (Public Policy)' },
    { value: 'cloud_gov', label: 'Cloud Engineer (GovCloud)' },
    { value: 'gis_developer_gov', label: 'GIS Developer (Public Infrastructure)' }
  ]
};

// Use a single reactive object to hold all form data
const formData = ref({
  sector: '',
  roles: [], // For the dynamic 'Other' text boxes, e.g., {'Architecture Technology': 'System Architect'}
  roleOther: '',
  ambition: null,       // For Q3 (radio button)
  passion: [],          // For Q4 (checkboxes)
  confidence: null,     // For Q5 (radio button)
  learningStyle: [],    // For Q6 (checkboxes)
  techPreference: null, // For Q7 (radio button)
  workPace: null,       // For Q8 (radio button)
});
const isRoleOtherSelected = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

// --- DYNAMIC LOGIC ---

// Computed property for predefined roles (no change here)
const dynamicRoleOptions = computed(() => {
  const selectedSector = formData.value.sector;
  if (!selectedSector) return [];
  if (selectedSector === 'idk') return generalRoles;
  return rolesBySector[selectedSector] || [];
});

// Watcher to reset roles when the sector changes
watch(() => formData.value.sector, () => {
  formData.value.roles = [];
  formData.value.roleOther = '';
  isRoleOtherSelected.value = false;
});
// Watcher to clear the "Other" text box if the checkbox is unticked
watch(isRoleOtherSelected, (isSelected) => {
  if (!isSelected) {
    formData.value.roleOther = '';
  }
});
// --- FORM SUBMISSION ---
async function handleSubmit() {
  isLoading.value = true;
  errorMessage.value = '';

  // Create the final payload object with all the data
  const payload = {
    cv_skills: props.cvSkills,
    questionnaire_answers: formData.value
  };

  console.log("Sending final payload to backend:", payload);

  try {
    // This is where you would make the API call to the final backend endpoint
    // For now, we will simulate it. Saul will build the real endpoint.
    // const response = await axios.post("http://127.0.0.1:8000/api/generate-roadmap", payload);

    // --- SIMULATION FOR NOW ---
    await new Promise(resolve => setTimeout(resolve, 1500)); // Pretend to wait for the API
    console.log("Simulated success! Data sent to backend.");
    // In the future, you would navigate to the results page here.
    // --- END SIMULATION ---
    
  } catch (error) {
    console.error("Error submitting questionnaire:", error);
    errorMessage.value = "There was an error submitting your answers.";
  } finally {
    isLoading.value = false;
  }
}
</script>









<style scoped>
.questionnaire-container {
  width: 700px;
  margin: 2rem auto;
  padding: 2.5rem;
  border: 1px solid var(--accent-color); /* ADDED: Accent border */
  border-radius: 8px;
  background-color: var(--background-color); 
}

.main-title {
  min-height: 2.5rem; /* Give it some space to type into */
  font-size: 1.75rem; /* Make the title a bit bigger */
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
fieldset {
  border: none;
  padding: 0;
  margin: 0;
}
legend, label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 700; 
}

button {
  background-color: var(--accent-color);
  color: var(--background-color); /* CHANGED: Use dark background for text */
  width: 100%;
  border: 0;
  padding: 12px 0;
  margin-top: 1rem;
  text-align: center;
  font-weight: bold;
  font-size: 16px;
  cursor: pointer;
  border-radius: 4px; 
}

.checkbox-group {
  padding-left: 10px;
}
input[type="checkbox"], input[type="radio"] {
  accent-color: var(--accent-color);
  margin-right: 0.5rem;
}
.other-group {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(224, 224, 224, 0.2);}
.other-input {
  width: 100%;
  padding: 8px;
  background-color: var(--background-color); 
  color: var(--text-color); 
  border: 1px solid var(--accent-color); 
  border-radius: 4px;
  margin-top: 0.5rem;
}

/* Style for disabled checkboxes to give user feedback */
.checkbox-group input:disabled + span {
  opacity: 0.5;
  text-decoration: line-through;
}
</style>