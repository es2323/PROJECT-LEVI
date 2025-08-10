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
        <label>What tech sector(s) are you most passionate about pursuing?</label>
        <MultiSelectDropdown 
          :options="sectorOptions"
          v-model="formData.sectors"
          placeholder="Select sectors..."
        />
      </div>

      <div v-if="formData.sectors.length > 0" class="form-group">
        <label>What type of role(s) do you see yourself doing? Don't worry if you aren't sure yet.</label>
        <div v-for="role in dynamicRoleOptions" :key="role.value" class="checkbox-group">
          <label>
            <input type="checkbox" :value="role.value" v-model="formData.roles.predefined">
            {{ role.label }}
          </label>
        </div>

        <div class="other-group">
          <label>Enter a custom role!</label>
          <input type="text" placeholder="e.g., Technical Writer" v-model="formData.roles.genericOther">
        </div>
        <div v-for="customSector in customSectors" :key="customSector" class="other-group">
          <label>What do you have in mind for '{{ customSector }}'?</label>
          <input type="text" placeholder="Specify role..." v-model="formData.roles.customSectorRoles[customSector]">
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
import MultiSelectDropdown from './MultiSelectDropdown.vue';
import Typewriter from './Typewriter.vue';
import axios from 'axios';

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
  { value: 'gov', label: 'GovTech & Public Sector 🏛️' }
]);

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
  sectors: [],
  roles: {
    predefined: [],      // For checkboxes, e.g., ['quant_dev']
    genericOther: '',    // For the main 'Other' text box
    customSectorRoles: {} // For the dynamic 'Other' text boxes, e.g., {'Architecture Technology': 'System Architect'}
  },
  ambition: null,       // For Q3 (radio button)
  passion: [],          // For Q4 (checkboxes)
  confidence: null,     // For Q5 (radio button)
  learningStyle: [],    // For Q6 (checkboxes)
  techPreference: null, // For Q7 (radio button)
  workPace: null,       // For Q8 (radio button)
});

// --- DYNAMIC LOGIC ---

// Computed property for predefined roles (no change here)
const dynamicRoleOptions = computed(() => {
  console.log("Sectors changed:", formData.value.sectors); 
  if (formData.value.sectors.length === 0) return [];
  
  // Use flatMap to get a single list of roles from all selected sectors
  return formData.value.sectors
    .filter(sector => rolesBySector[sector])
    .flatMap(sector => rolesBySector[sector]);
});

// 2. NEW COMPUTED PROPERTY for custom sectors
const customSectors = computed(() => {
  // Find selections that start with 'other:', then extract the text after the colon
  return formData.value.sectors
    .filter(s => s.startsWith('other:'))
    .map(s => s.split(':')[1]);
});

// Watcher to clean up role data when sectors change (slightly updated)
watch(() => formData.value.sectors, () => {
    const validRoleValues = dynamicRoleOptions.value.map(option => option.value);
    formData.value.roles.predefined = formData.value.roles.predefined.filter(role => validRoleValues.includes(role));
    
    // Clean up custom roles if the custom sector was removed
    for (const sectorName in formData.value.roles.customSectorRoles) {
        if (!customSectors.value.includes(sectorName)) {
            delete formData.value.roles.customSectorRoles[sectorName];
        }
    }
});

const props = defineProps({
  cvSkills: Array
});

const isLoading = ref(false); // Add refs for loading and error states
const errorMessage = ref('');

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
  width: 400px;
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

label {
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
input[type="checkbox"] {
  accent-color: var(--accent-color);
  margin-right: 0.5rem;
}
.other-group {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(224, 224, 224, 0.2);}
.other-group input {
  width: 100%;
  padding: 8px;
  background-color: var(--background-color); 
  color: var(--text-color); 
  border: 1px solid var(--accent-color); 
  border-radius: 4px;
  margin-top: 0.5rem;
}
</style>