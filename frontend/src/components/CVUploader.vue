<template>
  <div 
class="cv-uploader" 
    :class="{ 'is-dragging': isDragging }"
    @dragover.prevent="handleDragOver"
    @dragleave.prevent="handleDragLeave"
    @drop.prevent="handleDrop"
    
  >
    <div class="test-controls">
      <button @click="toggleLoadingTest" type="button" class="test-button">Toggle Loader</button>
      <button @click="emit('cv-uploaded')" type="button" class="test-button">Skip to Questionnaire</button>
      <button @click="emit('skip-to-roadmap')" type="button" class="test-button">Skip to Roadmap</button>
    </div>
    <!-- STAGE 1: The Initial Drop Zone -->
    <div v-if="!selectedFile && !isLoading" class="drop-zone-content">
      <svg class="upload-icon" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="17 8 12 3 7 8"></polyline>
        <line x1="12" y1="3" x2="12" y2="15"></line>
      </svg>
      <p class="drop-zone-title">Drag & Drop Your CV</p>
      <p class="browse-text">or</p>
      <label for="cv-upload-input" class="file-upload-label">Browse Files</label>
      <input id="cv-upload-input" type="file" @change="handleFileChange" accept=".pdf" class="file-input-hidden" />
    </div>

    <!-- STAGE 2: The Confirmation Screen -->
    <div v-if="selectedFile && !isLoading" class="confirmation-content">
      <svg class="pdf-icon" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10 9 9 9 8 9"></polyline>
      </svg>
      <p class="file-name-display">{{ selectedFile.name }}</p>
      <button @click="removeFile" type="button" class="remove-file-button">Remove File</button>
      <button @click="handleSubmit" type="button" class="submit-button">Analyse CV</button>
    </div>
    
    <!-- STAGE 3: The Loading Screen -->
    <div v-if="isLoading" class="spinner-container">
      <SvgLoader :loading-text="loadingStatus" />
    </div>
    <!-- Error Message Display -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'; 
import axios from 'axios';
import SvgLoader from './SvgLoader.vue';

// Create reactive variables to hold the selected file and the extracted text
const emit = defineEmits(['cv-uploaded', 'skip-to-roadmap']);
const selectedFile = ref(null);
const errorMessage = ref('');
const isLoading = ref(false);
const isDragging = ref(false);
const loadingStatus = ref('');

function toggleLoadingTest() {
  isLoading.value = !isLoading.value;

  // If we are turning the loader ON, set a sample status text
  if (isLoading.value) {
    loadingStatus.value = "Testing loading animation...";
  }
}
// --- File Handling Logic ---

// A single function to handle the file once it's selected (either by browse or drop)
function handleFileSelect(file) {
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file;
    errorMessage.value = '';
  } else {
    selectedFile.value = null;
    errorMessage.value = 'Please select a valid PDF file.';
  }
}

// Triggered by the hidden file input
function handleFileChange(event) {
  const file = event.target.files[0];
  handleFileSelect(file);
}

// --- Drag and Drop Logic ---

function handleDragOver() {
  isDragging.value = true;
}

function removeFile() {
  selectedFile.value = null;
}

function handleDragLeave() {
  isDragging.value = false;
}

function handleDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  handleFileSelect(file);
}

// --- Form Submission Logic ---

async function handleSubmit() {
  if (!selectedFile.value) {
    errorMessage.value = "Please select a file before submitting.";
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  // 2. Start cycling through loading messages
  const statuses = [
    "Connecting to server...",
    "Extracting text from your CV...",
    "AI is analyzing your skills...",
    "Finalizing results..."
  ];
  let statusIndex = 0;
  loadingStatus.value = statuses[statusIndex];

  const statusInterval = setInterval(() => {
    statusIndex++;
    if (statusIndex < statuses.length) {
      loadingStatus.value = statuses[statusIndex];
    } else {
      // If we run out of messages, just hold on the last one
      clearInterval(statusInterval);
    }
  }, 2000); // Change message every 2 seconds

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    const response = await axios.post("http://127.0.0.1:8000/api/cv-skill-extraction", formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    console.log("Full API Response Data:", response.data);
    emit('cv-uploaded', response.data.skills);

  } catch (error) {
    console.error("Error uploading file:", error);
    errorMessage.value = "An error occurred while uploading the file.";
  } finally {
    // 3. Clean up when done
    clearInterval(statusInterval);
    isLoading.value = false;
  }
}
</script>



<style scoped>

.cv-uploader {
  width: 100%;
  max-width: 700px;
  text-align: center;
  background: rgba(251, 251, 251, 0.05);
  
  /* The blur effect */
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  
  /* A subtle border to define the edge of the glass */
  border: 1px solid rgba(251, 251, 251, 0.1);
  
  /* A slightly larger radius looks better with glass */
  border-radius: 12px; 
  
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);

}
.cv-uploader.is-dragging {
  border-style: dashed;
  border-radius: 12px;
  background-color: rgba(197, 176, 205, 0.05); /* Use your new accent color */
}

.drop-zone-content {
  padding: 3rem;
  border: 2px dashed rgba(251, 251, 251, 0.2);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
.upload-icon {
  stroke: var(--accent-color);
  opacity: 0.8;
  animation: pulse 2.5s infinite; /* ADDED: Pulsing animation */
}

/* NEW: Style for the main title */
.drop-zone-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-color);
  margin: 0.5rem 0;
}

.browse-text {
  font-size: 1rem; /* CHANGED: Unified font size, made it slightly smaller than main text */
  opacity: 0.7;
}

.file-upload-label {
  width: 40%;
  padding: 0.75rem 1.5rem;
  background-color: var(--accent-color); 
  color: var(--background-color);
  font-weight: 700; 
  font-size: 1rem;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s;
  display: inline-block;
}

.file-upload-label:hover {
  transform: scale(1.05); /* ADDED: A more interactive hover effect */
}

.file-input-hidden {
  display: none; 
}

.confirmation-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
}

.pdf-icon {
  stroke: var(--accent-color);
  margin-bottom: 1rem;
}

.file-name-display {
  font-weight: 500;
  font-size: 1.1rem;
  color: var(--text-color);
}

.remove-file-button {
  background: none;
  border: none;
  color: var(--text-color);
  opacity: 0.6;
  text-decoration: underline;
  cursor: pointer;
  margin-top: -0.5rem; /* Tucks it closer to the filename */
  margin-bottom: 1.5rem;
}

.submit-button {
  width: 40%;
  padding: 1rem 1.5rem;
  background-color: var(--accent-color);
  color: var(--background-color);
  font-weight: 700;
  font-size: 1rem;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: transform 0.2s;
}

.submit-button:hover {
  transform: scale(1.02);
}

/* NEW: Keyframes for the pulsing icon */
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.05);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0.8;
}

}
.spinner-container {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}


.test-button {
  margin-top: 1rem;
  background: none;
  border: 1px solid var(--accent-color);
  color: var(--accent-color);
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 4px;
}
</style>