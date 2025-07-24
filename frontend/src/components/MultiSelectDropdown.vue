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
  font-family: "Andale Mono", AndaleMono, monospace;
}
.dropdown-button {
  width: 100%;
  background-color: #4F6877;
  color: #fff;
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  text-align: left;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}
.dropdown-menu {
  position: absolute;
  width: 100%;
  background-color: #4F6877;
  border-radius: 4px;
  margin-top: 4px;
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
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
  color: #fff;
}
li:hover {
  background-color: #374954;
}
input[type="checkbox"] {
  margin-right: 10px;
}
.other-input {
  width: calc(100% - 20px);
  margin: 0 10px 10px 10px;
  padding: 8px;
  border: 1px solid #374954;
  background-color: #fff;
  color: #333;
  border-radius: 4px;
}
.arrow {
  font-size: 10px;
}
</style>