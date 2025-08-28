<template>
  <div
    class="cv-uploader"
    :class="{ 'is-dragging': isDragging }"
    @dragover.prevent="handleDragOver"
    @dragleave.prevent="handleDragLeave"
    @drop.prevent="handleDrop"
  >
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

    <div v-if="isLoading" class="spinner-container">
      <div class="spinner"></div>
      <p class="loading-text">{{ loadingStatus }}</p>
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
// Import the central API client
import apiClient from '../api';

const emit = defineEmits(['cv-uploaded']);
const selectedFile = ref(null);
const errorMessage = ref('');
const isLoading = ref(false);
const isDragging = ref(false);
const loadingStatus = ref('');

// --- File Handling Logic ---
function handleFileSelect(file) { if (file && file.type === 'application/pdf') { selectedFile.value = file; errorMessage.value = ''; } else { selectedFile.value = null; errorMessage.value = 'Please select a valid PDF file.'; } }
function handleFileChange(event) { const file = event.target.files[0]; handleFileSelect(file); }
function removeFile() { selectedFile.value = null; }

// --- Drag and Drop Logic ---
function handleDragOver() { isDragging.value = true; }
function handleDragLeave() { isDragging.value = false; }
function handleDrop(event) { isDragging.value = false; const file = event.dataTransfer.files[0]; handleFileSelect(file); }

// --- Form Submission Logic ---
async function handleSubmit() {
  if (!selectedFile.value) { /* ... */ return; }
  isLoading.value = true;
  errorMessage.value = '';
  loadingStatus.value = 'Analysing your skills...';

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    const response = await apiClient.post("/cv-skill-extraction", formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    if (response.data.session_token) {
      localStorage.setItem('session_token', response.data.session_token);
    }

    emit('cv-uploaded', response.data.skills);

  } catch (error) {
    console.error("Error uploading file:", error);
    errorMessage.value = "An error occurred while uploading the file.";
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.cv-uploader {
  width: 100%;
  max-width: 650px;
  margin: 2rem auto;
  padding: 2.5rem;
  border: 2px solid var(--accent-color);
  border-radius: 8px;
  text-align: center;
  transition: background-color 0.3s, border-style 0.3s;
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
  gap: 0.5rem;
  color: var(--text-color);
  opacity: 0.7;
}

.drop-zone-content svg {
  stroke: var(--accent-color);
}

.browse-text {
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.file-upload-label {
  padding: 0.5rem 1rem;
  background-color: var(--accent-color);
  color: var(--background-color);
  font-weight: 700;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: inline-block;
}

.file-upload-label:hover {
  background-color: #cda240;
}

.file-input-hidden {
  display: none;
}

.file-name-container {
  margin-top: 1rem;
}

.file-name {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-color);
  opacity: 0.9;
}

.submit-button {
  width: 100%;
  margin-top: 1.5rem;
  padding: 0.75rem 1rem;
  background-color: var(--accent-color);
  color: var(--background-color);
  font-weight: 700;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.submit-button:disabled {
  background-color: #8c7127;
  cursor: not-allowed;
  opacity: 0.6;
}

.spinner-container {
  margin-top: 1.5rem;
  text-align: center;
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