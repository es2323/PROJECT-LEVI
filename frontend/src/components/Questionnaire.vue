<template>
  <div class="questionnaire-container">
    <div class="progress-text">
      Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}
    </div>
    <div class="progress-bar-container">
      <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
    </div>
    <Transition name="fade" mode="out-in">
      <div v-if="currentQuestion" class="question-wrapper" :key="currentQuestion.id">
        <fieldset class="form-group">
          <legend>{{ currentQuestion.text }}</legend>
          
          <div v-if="currentQuestion.type === 'select'" class="options-group">
            <CustomDropdown
              v-model="answers[currentQuestion.id]"
              :options="currentQuestion.options"
              placeholder="Please select one"
            />
          </div>

          <div v-if="currentQuestion.type === 'checkbox'" class="options-group">
            <label v-for="option in currentQuestion.options" :key="option.value">
              <input 
                type="checkbox"
                :value="option.value"
                :checked="isOptionChecked(currentQuestion.id, option.value)"
                @change="handleCheckboxChange(currentQuestion.id, option.value, option.exclusive)"
                :disabled="isCheckboxDisabled(currentQuestion.id, option.value)"
              >
              {{ option.label }}
            </label>
          </div>

          <div v-if="currentQuestion.type === 'radio'" class="options-group">
            <label v-for="option in currentQuestion.options" :key="option.value">
              <input type="radio" :name="currentQuestion.id" :value="option.value" v-model="answers[currentQuestion.id]">
              {{ option.label }}
            </label>
          </div>
        </fieldset>
        <div class="navigation-buttons">
          <button v-if="currentQuestionIndex > 0" @click="previousQuestion" type="button" class="prev-button">
            Previous
          </button>
          <button v-if="currentQuestionIndex < questions.length - 1" @click="nextQuestion" type="button" class="next-button">
            Next
          </button>
          <button v-else @click="handleSubmit" type="button" class="submit-button">
            Generate My Roadmap
          </button>
        </div>

      </div>
    </Transition>
  </div>
</template>




<script setup>
import { ref, computed, watch } from 'vue';
import CustomDropdown from './CustomDropdown.vue';

// --- DATA DEFINITIONS ---

// This helper object maps sectors to their specific roles
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
    { value: 'robotics_auto', label: 'Robotics Software Engineer'}
  ],
  gov: [
    { value: 'fullstack_citizen', label: 'Full-Stack Developer (Citizen Services)' },
    { value: 'cybersec_gov', label: 'Cybersecurity Analyst (Public Sector)' },
    { value: 'data_analyst_policy', label: 'Data Analyst (Public Policy)' },
    { value: 'cloud_gov', label: 'Cloud Engineer (GovCloud)' },
    { value: 'gis_developer_gov', label: 'GIS Developer (Public Infrastructure)' }
  ]
};

// This helper array holds the roles for the "IDK" option
const generalRoles = [
  { value: 'swe', label: 'Graduate Software Engineer' },
  { value: 'backend', label: 'Backend Developer' },
  { value: 'frontend', label: 'Frontend Developer' },
  { value: 'cloud', label: 'Cloud / DevOps Engineer' },
  { value: 'data_analyst', label: 'Data Analyst' }
];

// --- THE SINGLE QUESTIONS ARRAY ---
const questions = ref([
  {
    id: 'sector',
    text: "Which Tech Sector are you most passionate about pursuing?",
    type: 'select',
    options: [
      { value: 'idk', label: "I'm not sure yet, give me general Tech roles" }, 
      { value: 'fintech', label: 'Financial Tech' },
      { value: 'healthtech', label: 'HealthTech' },
      { value: 'ai_ml', label: 'AI / Machine Learning' },
      { value: 'ecommerce', label: 'E-commerce & Retail' },
      { value: 'game', label: 'Gaming & Entertainment' },
      { value: 'edtech', label: 'EdTech' },
      { value: 'greentech', label: 'GreenTech & Sustainability' },
      { value: 'cars', label: 'Automotive & Transportation' },
      { value: 'gov', label: 'GovTech & Public Sector' },
    ]
  },
  {
    id: 'roles',
    text: "What type of roles do you see yourself doing? (Select up to 3)",
    type: 'checkbox',
    limit: 3,
    options: [] // This will be filled dynamically
  },
  {
    id: 'ambition',
    text: "Looking ahead 5 years, what is your primary professional goal?",
    type: 'radio',
    options: [
      { value: 'unsure', label: "I'm not too sure yet" },
      { value: 'expert', label: 'I see myself as a Senior Technical expert' },
      { value: 'leadership', label: 'I want to be involved in Team Leadership' },
      { value: 'product', label: "I'd prefer a Product-Focused role" },
    ]
  },
  {
    id: 'passion',
    text: "Here are some foundational software engineering concepts, which do you feel you have the least practical experience in?",
    type: 'checkbox',
    limit: 3,
    options: [
      { value: 'code', label: 'Writing efficient, production-quality code.' },
      { value: 'DB', label: 'Storing and managing data effectively e.g., with databases' },
      { value: 'integrate', label: 'Connecting different parts of a system together e.g., frontend to backend.' },
      { value: 'automation', label: 'Automating infrastructure and deployment pipelines' },
      { value: 'idk', label: "I'm still new to all of these areas.", exclusive: true }

    ]
  },
  {
    id: 'confidence',
    text: "Think about your top technical skill... how would you rate your ability?",
    type: 'radio',
    options: [
      {value: 'unsure', label: "I don't have technical skills yet :/"},
      { value: 'foundational', label: "Foundational - I've mostly done tutorials" },
      { value: 'intermediate', label: "Intermediate - I've built a personal project" },
      { value: 'advanced', label: "Advanced - I'm ready for production code" }
    ]
  },
  {
    id: 'learningStyle',
    text: "What's the best way you learn?",
    type: 'checkbox',
    limit: 3,
    options: [
      { value: 'visual', label: "I'm a visual learner (diagrams, videos)" },
      { value: 'auditory', label: "I'm an auditory learner (listening to lectures, discussions)"},
      { value: 'reading', label: "I prefer reading & writing (notes, articles, books)"},
      { value: 'kinaesthetic', label: "I'm more practical (project based learning, shadowing)" }
    ]
  },
  {
    id: 'techPreference',
    text: "What's your typical approach to learning something new?",
    type: 'radio',
    options: [
      { value: 'cutting-edge', label: "I dive straight into the latest, cutting-edge tech" },
      { value: 'stable', label: "I prefer a stable & widely adopted tech framework" },
      { value: 'mix', label: "I'd like a mix of both" }
    ]
  },
  {
    id: 'workPace',
    text: "Lets figure out your speed!",
    type: 'radio',
    options: [
      { value: 'fast', label: "I'm dynamic & fast-paced, learning bits about many different technologies" },
      { value: 'focused', label: "I prefer a stuctured & deep focused dive into mastering few technologies completely"}
    ]
  }
]);

// --- STATE MANAGEMENT ---
const currentQuestionIndex = ref(0);
const answers = ref({});

// --- DYNAMIC LOGIC ---
const currentQuestion = computed(() => questions.value[currentQuestionIndex.value]);
const progressPercentage = computed(() => ((currentQuestionIndex.value) / (questions.value.length - 1)) * 100);

// Watcher to dynamically populate the 'roles' question options
watch(() => answers.value.sector, (selectedSector) => {
  const rolesQuestion = questions.value.find(q => q.id === 'roles');
  if (rolesQuestion) {
    rolesQuestion.options = selectedSector === 'idk' ? generalRoles : (rolesBySector[selectedSector] || []);
    answers.value.roles = [];
  }
}, { immediate: true });

// NEW: Generic function to check if an option is selected
const isOptionChecked = (questionId, optionValue) => {
  const answer = answers.value[questionId];
  return Array.isArray(answer) && answer.includes(optionValue);
};

// NEW: Generic function to disable checkboxes when the limit is reached
// In your <script setup> block

function isCheckboxDisabled(questionId, optionValue) {
  const question = questions.value.find(q => q.id === questionId);
  const answer = answers.value[questionId] || [];

  // 1. Find the exclusive option for this question, if it exists
  const exclusiveOption = question.options.find(opt => opt.exclusive)?.value;

  // 2. Check if the exclusive option is currently selected
  if (exclusiveOption && answer.includes(exclusiveOption)) {
    // If it is, disable every *other* option
    return optionValue !== exclusiveOption;
  }

  // 3. If the exclusive option is not selected, apply the selection limit
  if (question && question.limit) {
    return answer.length >= question.limit && !answer.includes(optionValue);
  }

  // Otherwise, the checkbox is not disabled
  return false;
}

// NEW: Generic handler for all checkbox clicks
function handleCheckboxChange(questionId, optionValue, isExclusive = false) {
  // Ensure the answer is an array
  if (!Array.isArray(answers.value[questionId])) {
    answers.value[questionId] = [];
  }
  
  const currentAnswers = answers.value[questionId];
  const isChecked = currentAnswers.includes(optionValue);
  
  if (isExclusive) {
    // If the exclusive option is checked, replace the array with only that option. Otherwise, clear it.
    answers.value[questionId] = isChecked ? [] : [optionValue];
    return;
  }

  if (isChecked) {
    // Uncheck the box: remove it from the array
    answers.value[questionId] = currentAnswers.filter(val => val !== optionValue);
  } else {
    // Check the box: add it to the array
    // First, remove any exclusive option that might be selected
    const question = questions.value.find(q => q.id === questionId);
    const exclusiveOpt = question.options.find(opt => opt.exclusive)?.value;
    let newAnswers = currentAnswers.filter(val => val !== exclusiveOpt);

    newAnswers.push(optionValue);
    answers.value[questionId] = newAnswers;
  }
}
// --- FORM NAVIGATION & SUBMISSION ---
function nextQuestion() {
  if (currentQuestionIndex.value < questions.value.length - 1) currentQuestionIndex.value++;
}

function previousQuestion() {
  if (currentQuestionIndex.value > 0) currentQuestionIndex.value--;
}

function handleSubmit() {
  console.log("Final Answers:", answers.value);
  // Logic to send 'answers.value' to the backend will go here
}
</script>









<style scoped>
/* --- Main Container & Layout --- */
.questionnaire-container {
  background: rgba(251, 251, 251, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(251, 251, 251, 0.1);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  width: 100%;
  max-width: 800px;
  margin: 2rem auto;
  padding: 3rem;
  text-align: center;
}
.question-wrapper { text-align: left; }

/* --- Typography --- */
.progress-text {
  text-align: center;
  margin-bottom: 0.75rem;
  font-weight: 500;
  opacity: 0.8;
}
legend {
  font-size: 1.4rem;
  font-weight: 400;
  margin-bottom: 1.5rem;
  line-height: 1.4;
}
.options-group label {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  font-weight: 100;
  margin-bottom: 1rem;
  cursor: pointer;
}

/* --- Progress Bar --- */
.progress-bar-container {
  width: 100%;
  height: 4px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  margin-bottom: 3rem;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  background-color: var(--accent-color);
  transition: width 0.4s ease-in-out;
}

/* --- Form Elements --- */
fieldset.form-group { border: none; padding: 0; margin: 0; }

input[type="checkbox"], input[type="radio"] {
  accent-color: var(--accent-color);
  margin-right: .75rem;
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}
label:has(input:disabled) {
  opacity: 0.5;
  cursor: not-allowed;
}

/* --- Navigation --- */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  border-top: 1px solid rgba(251, 251, 251, 0.1);
  padding-top: 2rem;
}
.prev-button, .next-button, .submit-button {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}
.prev-button {
  background-color: transparent;
  border: 1px solid var(--text-color);
  color: var(--text-color);
  opacity: 0.7;
}
.prev-button:hover { opacity: 1; }
.next-button, .submit-button {
  background-color: var(--accent-color);
  color: var(--background-color);
  margin-left: auto;
}
.next-button:hover, .submit-button:hover { opacity: 0.9; }

/* --- Transitions --- */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>