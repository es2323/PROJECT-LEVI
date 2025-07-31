<template>
  <div class="cv-uploader">
    <form @submit.prevent="handleSubmit" class="upload-form">
      
      <label for="cv-upload" class="file-upload-label">
        Choose PDF File
      </label>
      
      <input 
        id="cv-upload"
        type="file" 
        @change="handleFileChange"
        accept=".pdf" 
        class="file-input-hidden" 
      />

      <p v-if="selectedFile" class="file-name">
        Selected: {{ selectedFile.name }}
      </p>
      <p v-else class="file-name">No file chosen</p>
      
      <button type="submit" :disabled="isLoading || !selectedFile" class="submit-button">
        {{ isLoading ? 'Analysing...' : 'Analyse CV' }}
      </button>

    </form>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div v-if="extractedText" class="results-container">
      <h3>Extracted Text:</h3>
      <pre class="results-text">{{ extractedText }}</pre>
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

// This function now saves the selected file to our state
function handleFileChange(event) {
  // Logic for handling the selected file will go here
  selectedFile.value = event.target.files[0];
  console.log("File stored:", selectedFile.value);
}

async function handleSubmit() {
  // 1. Check if a file has been selected
  if (!selectedFile.value) {
    errorMessage.value = "Please select a file before submitting.";
    return;
  }

  // 2. Set loading state and clear previous messages
  isLoading.value = true;
  errorMessage.value = '';
  extractedText.value = '';

  // 3. Create a FormData object to send the file
  const formData = new FormData();
  formData.append("file", selectedFile.value); // The key "file" must match what FastAPI expects

  try {
    // 4. Make the POST request with axios
    const response = await axios.post("http://127.0.0.1:8000/api/cv-skill-extraction", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // 5. Handle the successful response
    console.log("API Response:", response.data);
    extractedText.value = response.data.extracted_skills;

  } catch (error) {
    // 6. Handle any errors from the API call
    console.error("Error uploading file:", error);
    errorMessage.value = "An error occurred while uploading the file. Please try again.";
  } finally {
    // 7. Reset the loading state
    isLoading.value = false;
    emit('cv-uploaded');  }
}
</script>

<style scoped>

.cv-uploader {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2.5rem;
  border: 1px solid var(--accent-color); 
  border-radius: 8px;
  text-align: center;
}
.cv-uploader-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.error-message {
  margin-top: 1rem;
  color:  #ff7f7f;/* Red color for errors */
  font-weight: bold;
}

.results-container {
  margin-top: 2rem;
  text-align: left;
  border-top: 1px solid rgba(224, 224, 224, 0.2);
  padding-top: 1rem;
}

.results-text {
  background-color: rgba(0, 0, 0, 0.2); 
  padding: 1rem;
  border-radius: 4px;
  white-space: pre-wrap; /* This makes the text wrap nicely */
  word-wrap: break-word;
  max-height: 300px;
  overflow-y: auto;
  color: var(--text-color); 
}

.file-upload-label {
  padding: 0.75rem 1rem;
  background-color: var(--accent-color); 
  color: var(--background-color);
  font-weight: 700; 
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: inline-block; /* Makes padding and other properties work well */
}

.file-upload-label:hover {
  background-color:  #cda240;
}

.file-input-hidden {
  display: none; 
}

.file-name {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-color); 
  opacity: 0.7
}

.submit-button { /* Added base styles for the submit button */
  padding: 0.75rem 1rem;
  background-color: var(--accent-color);
  color: var(--background-color);
  font-weight: 700;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.submit-button:disabled {
  background-color: #8c7127;/* Grey out the button when disabled */
  cursor: not-allowed;
  opacity: 0.6;

}
</style>