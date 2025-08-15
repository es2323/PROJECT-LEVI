<template>
  <!-- The main container for the uploader -->
  <div 
    class="cv-uploader" 
    :class="{ 'is-dragging': isDragging }"
    @dragover.prevent="handleDragOver"
    @dragleave.prevent="handleDragLeave"
    @drop.prevent="handleDrop"
  >
    <!-- This form now contains everything, including the drop zone content -->
    <form @submit.prevent="handleSubmit" class="upload-form">
      <!-- This is the visual drop zone area -->
      <div class="drop-zone-content">
        <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
          <polyline points="17 8 12 3 7 8"></polyline>
          <line x1="12" y1="3" x2="12" y2="15"></line>
        </svg>
        
        <p>Drag & Drop your CV here</p>
        <p class="browse-text">OR</p>
        
        <!-- The label acts as a button to trigger the hidden file input -->
        <label for="cv-upload-input" class="file-upload-label">
          Browse Files
        </label>
        <input id="cv-upload-input" type="file" @change="handleFileChange" accept=".pdf" class="file-input-hidden" />
      </div>

      <!-- This section shows the selected file name -->
      <div v-if="selectedFile" class="file-name-container">
        <p class="file-name">Selected: {{ selectedFile.name }}</p>
      </div>
      
      <!-- The main submit button -->
      <button v-if="!isLoading" type="submit" :disabled="!selectedFile" class="submit-button">
        Analyse CV
      </button>
    </form>

    <!-- This section shows the loading spinner -->
    <div v-if="isLoading" class="spinner-container">
      <div class="spinner"></div>
      <p>Analysing your skills...</p>
    </div>

    <!-- This section shows any error messages -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'; 
import axios from 'axios';

// Create reactive variables to hold the selected file and the extracted text
const emit = defineEmits(['cv-uploaded']);
const selectedFile = ref(null);
const extractedText = ref('');
const errorMessage = ref('');
const isLoading = ref(false);
const isDragging = ref(false);

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

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    const response = await axios.post("http://127.0.0.1:8000/api/cv-skill-extraction", formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    console.log("Full API Response Data:", response.data);
    // You can handle the extracted skills here later
    emit('cv-uploaded', response.data.skills);

  } catch (error) {
    console.error("Error uploading file:", error);
    errorMessage.value = "An error occurred while uploading the file. Please try again.";
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>

.cv-uploader {
  width: 100%;
  max-width: 1200px;
  margin: 2rem auto;
  padding: 3rem;
  border: 2px solid var(--accent-color); 
  border-radius: 1000px;
  text-align: center;
  transition: background-color 0.3s, border-style 0.3s;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); /* ADDED: A subtle shadow to lift the element */

}
.cv-uploader.is-dragging {
  border-style: dashed;
  background-color: rgba(227, 180, 72, 0.05);
}

.drop-zone-content {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  color: var(--text-color);
  opacity: 1;
  font-size: 2rem; /* ADDED: A larger, unified font size for this section */

}

.drop-zone-content svg {
  width: 80px; /* ADDED: Made the icon bigger */
  height: 80px;
  stroke: var(--accent-color);
  opacity: 0.8;
}

.browse-text {
  font-size: 1rem; /* CHANGED: Unified font size, made it slightly smaller than main text */
  margin: 0; /* REMOVED: Simplified margin */
  opacity: 0.7;
}

.file-upload-label {
  width: 20%;
  padding: 0.75rem 1.5rem;
  background-color: var(--accent-color); 
  color: var(--background-color);
  font-weight: 700; 
  font-size: 1rem;
  border-radius: 40px;
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

.file-name-container {
  margin-top: 1rem;
}

.file-name {
  font-size: 1rem;
  color: var(--text-color); 
  opacity: 0.9;
}

.submit-button {
  width: 50%;
  margin-top: 1.5rem;
  padding: 1rem 1.5rem;
  background-color: var(--accent-color);
  color: var(--background-color);
  font-weight: 700;
  font-size: 1.25rem; /* CHANGED: Made font bigger */

  border-radius: 50px;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s; /* ADDED: Transition for disabled state */

}

.submit-button:disabled {
  background-color: var(--accent-color);
  cursor: not-allowed;
  opacity: 0.6;

}

/* Add this new class for visual feedback */
.cv-uploader.is-dragging {
  border-style: dashed;
  border-color: var(--accent-color);
  background-color: rgba(227, 180, 72, 0.1); /* Faint accent color */
}
.spinner-container {
  margin-top: 1.5rem;
}
.spinner {
  border: 4px solid rgba(224, 224, 224, 0.3);
  border-top: 4px solid var(--accent-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.error-message {
  margin-top: 1rem;
  color: #ff7f7f;
  font-weight: bold;
}
</style>