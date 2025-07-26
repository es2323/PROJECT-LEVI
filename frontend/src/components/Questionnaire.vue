<template>
  <div class="questionnaire-container">
    <h2>Tell us more about your goals!</h2>
    <p class="subtitle">This will help us build the perfect roadmap for you.</p>
    
    <form @submit.prevent="handleSubmit" class="form-wrapper">
      <div class="form-group">
        <label>What tech sector(s) are you most passionate about pursuing?</label>
        <MultiSelectDropdown 
          :options="sectorOptions"
          v-model="formData.sectors"
          placeholder="Select sectors..."
        />
      </div>

      <div class="form-group">
        <label>What type of role(s) do you see yourself doing?</label>
        <MultiSelectDropdown 
          :options="dynamicRoleOptions"
          v-model="formData.roles"
          placeholder="Select roles..."
        />
      </div>
      
      <button type="submit">Generate My Roadmap</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import MultiSelectDropdown from './MultiSelectDropdown.vue';

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
  roles: [],
});

// --- DYNAMIC LOGIC ---

// 2. THE COMPUTED PROPERTY: Automatically generates the role options
const dynamicRoleOptions = computed(() => {
  console.log("Sectors changed:", formData.value.sectors); 
  if (formData.value.sectors.length === 0) {
    return [];
  }
  // Use flatMap to get a single list of roles from all selected sectors
  return formData.value.sectors
    .filter(sector => rolesBySector[sector]) // Filter out 'other' selections
    .flatMap(sector => rolesBySector[sector]);
});

// 4. THE WATCHER: Cleans up selected roles if a sector is deselected
watch(() => formData.value.sectors, (newSectors, oldSectors) => {
  // If sectors were removed, we need to check if any selected roles are now invalid
  if (newSectors.length < oldSectors.length) {
    const validRoleValues = dynamicRoleOptions.value.map(option => option.value);
    // Filter the roles to keep only those that are still valid
    formData.value.roles = formData.value.roles.filter(role => {
      // Keep 'other' selections, but remove specific roles that are no longer valid
      return role.startsWith('other') || validRoleValues.includes(role);
    });
  }
});

function handleSubmit() {
  console.log("Final form data:", formData.value);
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