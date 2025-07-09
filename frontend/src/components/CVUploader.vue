<template>
  <div class="cv-uploader">
    <h2>Upload Your CV</h2>
    <p>Provide your CV in PDF format to begin the analysis.</p>

    <form @submit.prevent="handleSubmit" class="cv-uploader-form">
      <label for="cv-input">Select PDF File:</label>
      <input 
        id="cv-input"
        type="file" 
        accept=".pdf"
        @change="handleFileChange" 
      />
      <button type="submit">Analyse CV</button>
    </form>
  </div>
</template>

<script setup>
// Using camelCase for function names for readability
function handleFileChange(event) {
  // Logic for handling the selected file will go here
  console.log("File selected:", event.target.files[0]);
}

function handleSubmit() {
  // This is where we will later EMIT an event to the parent component
  // This follows the "Clear Data Flow" principle
  console.log("Form submitted!");
}
</script>

<style scoped>
/* This is a "Smart Styling Strategy" */
/* These styles ONLY apply to this component and won't leak out */
.cv-uploader {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: center;
}
.cv-uploader-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}
</style>