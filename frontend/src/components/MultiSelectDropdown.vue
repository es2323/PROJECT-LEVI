<template>
  <div class="dropdown-container">
    <button @click="toggleDropdown" type="button" class="dropdown-button">
      <span>{{ buttonLabel }}</span>
      <span class="arrow">{{ isOpen ? '▲' : '▼' }}</span>
    </button>
    <div v-if="isOpen" class="dropdown-menu">
      <ul>
        <li v-for="option in options" :key="option.value">
          <label>
            <input type="checkbox" :value="option.value" v-model="selectedValues" @change="emitUpdate"/>
            {{ option.label }}
          </label>
        </li>
        <li>
          <label>
            <input type="checkbox" value="other" v-model="isOtherSelected" />
            Other
          </label>
        </li>
      </ul>
      <input 
        v-if="isOtherSelected" 
        type="text" 
        v-model="otherValue" 
        @input="emitUpdate"
        placeholder="Please specify" 
        class="other-input"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  options: Array, // e.g., [{ value: 'frontend', label: 'Frontend' }]
  modelValue: Array, // for v-model binding
  placeholder: {
    type: String,
    default: 'Select options'
  }
});

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);
const selectedValues = ref([...props.modelValue.filter(v => v !== 'other' && !v.startsWith('other:'))]);
const isOtherSelected = ref(props.modelValue.some(v => v === 'other' || v.startsWith('other:')));
const initialOtherValue = props.modelValue.find(v => v.startsWith('other:'))?.split(':')[1] || '';
const otherValue = ref(initialOtherValue);

function toggleDropdown() {
  isOpen.value = !isOpen.value;
}

const buttonLabel = computed(() => {
  if (selectedValues.value.length === 0 && !otherValue.value) {
    return props.placeholder;
  }
  let labels = [...selectedValues.value];
  if (otherValue.value) {
    labels.push(`Other (${otherValue.value})`);
  }
  return labels.join(', ');
});

function emitUpdate() {
  let finalValues = [...selectedValues.value];
  if (isOtherSelected.value) {
    finalValues.push('other');
    if (otherValue.value.trim()) {
      finalValues.push(`other:${otherValue.value.trim()}`);
    }
  }
  emit('update:modelValue', finalValues);
}

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
    selectedValues.value = [...newValue.filter(v => v !== 'other' && !v.startsWith('other:'))];
    isOtherSelected.value = newValue.some(v => v === 'other' || v.startsWith('other:'));
    otherValue.value = newValue.find(v => v.startsWith('other:'))?.split(':')[1] || '';
});
</script>

<style scoped>
.dropdown-container {
  position: relative;
  width: 100%;
}
.dropdown-button {
  width: 100%;
  background-color: var(--accent-color); /* CHANGED: Use accent color */
  color: var(--background-color); /* CHANGED: Use dark background for text */
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  text-align: left;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 700; /* ADDED: Make text bold */
  font-size: 14px;
}
.dropdown-menu {
  position: absolute;
  width: 100%;
  background-color: #2a4a40;
  border-radius: 4px;
  margin-top: 4px;
  z-index: 10;
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid var(--accent-color);
}
ul {
  list-style: none;
  margin: 0;
  padding: 10px;
}
li label {
  display: flex;
  align-items: center;
  padding: 8px;
  cursor: pointer;
  color: var(--text-color);
}
li:hover {
  background-color: var(--background-color);
}
input[type="checkbox"] {
  margin-right: 10px;
  accent-color: var(--accent-color);
}
.other-input {
  width: calc(100% - 50px);
  margin: 0 10px 10px 10px;
  padding: 8px;
  border: 1px solid var(--accent-color); 
  background-color: var(--background-color); 
  color: var(--text-color); 
  border-radius: 4px;
}
.arrow {
  font-size: 10px;
}
</style>