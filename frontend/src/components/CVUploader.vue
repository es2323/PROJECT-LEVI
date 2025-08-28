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
      <SvgLoader :loading-text="loadingStatus" />
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import apiClient from '../api';
import SvgLoader from './SvgLoader.vue';

const emit = defineEmits(['cv-uploaded']);
const selectedFile = ref(null);
const errorMessage = ref('');
const isLoading = ref(false);
const isDragging = ref(false);
const loadingStatus = ref('');

// --- All file handling and drag/drop logic from the FDV is correct ---
function handleFileSelect(file) { if (file && file.type === 'application/pdf') { selectedFile.value = file; errorMessage.value = ''; } else { selectedFile.value = null; errorMessage.value = 'Please select a valid PDF file.'; } }
function handleFileChange(event) { const file = event.target.files[0]; handleFileSelect(file); }
function removeFile() { selectedFile.value = null; }
function handleDragOver() { isDragging.value = true; }
function handleDragLeave() { isDragging.value = false; }
function handleDrop(event) { isDragging.value = false; const file = event.dataTransfer.files[0]; handleFileSelect(file); }

async function handleSubmit() {
  if (!selectedFile.value) { return; }
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
/* All styles from the frontend dev's version are correct */
.cv-uploader { width: 100%; max-width: 700px; text-align: center; background: rgba(251, 251, 251, 0.05); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(251, 251, 251, 0.1); border-radius: 12px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); }
.cv-uploader.is-dragging { border-style: dashed; border-radius: 12px; background-color: rgba(197, 176, 205, 0.05); }
.drop-zone-content { padding: 3rem; border: 2px dashed rgba(251, 251, 251, 0.2); border-radius: 12px; display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.upload-icon { stroke: var(--accent-color); opacity: 0.8; animation: pulse 2.5s infinite; }
.drop-zone-title { font-size: 2rem; font-weight: 700; color: var(--text-color); margin: 0.5rem 0; }
.browse-text { font-size: 1rem; opacity: 0.7; }
.file-upload-label { width: 40%; padding: 0.75rem 1.5rem; background-color: var(--accent-color); color: var(--background-color); font-weight: 700; font-size: 1rem; border-radius: 12px; cursor: pointer; transition: transform 0.2s; display: inline-block; }
.file-upload-label:hover { transform: scale(1.05); }
.file-input-hidden { display: none; }
.confirmation-content { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 2rem; }
.pdf-icon { stroke: var(--accent-color); margin-bottom: 1rem; }
.file-name-display { font-weight: 500; font-size: 1.1rem; color: var(--text-color); }
.remove-file-button { background: none; border: none; color: var(--text-color); opacity: 0.6; text-decoration: underline; cursor: pointer; margin-top: -0.5rem; margin-bottom: 1.5rem; }
.submit-button { width: 40%; padding: 1rem 1.5rem; background-color: var(--accent-color); color: var(--background-color); font-weight: 700; font-size: 1rem; border-radius: 12px; border: none; cursor: pointer; transition: transform 0.2s; }
.submit-button:hover { transform: scale(1.02); }
@keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.05); opacity: 1; } 100% { transform: scale(1); opacity: 0.8; } }
.spinner-container { margin-top: 1.5rem; display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.error-message { margin-top: 1rem; color: #ff7f7f; font-weight: bold; }
</style>