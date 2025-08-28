<template>
  <div class="dropdown-container">
    <button @click="isOpen = !isOpen" type="button" class="dropdown-button">
      <span>{{ selectedLabel }}</span>
      <span class="arrow">{{ isOpen ? '▲' : '▼' }}</span>
    </button>
    <div v-if="isOpen" class="dropdown-menu">
      <ul>
        <li v-for="option in options" :key="option.value" @click="selectOption(option)">
          {{ option.label }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  options: Array,
  modelValue: String, // The v-model value
  placeholder: {
    type: String,
    default: 'Please select one'
  }
});

const emit = defineEmits(['update:modelValue']);
const isOpen = ref(false);

const selectedLabel = computed(() => {
  const selected = props.options.find(opt => opt.value === props.modelValue);
  return selected ? selected.label : props.placeholder;
});

function selectOption(option) {
  emit('update:modelValue', option.value);
  isOpen.value = false;
}
</script>

<style scoped>
.dropdown-container {
  position: relative;
  width: 100%;
}
.dropdown-button {
  width: 100%;
  padding: 0.75rem 1rem;
  font-family: 'Satoshi', sans-serif;
  font-size: 1rem;
  cursor: pointer;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;

  /* The Glass Effect */
  background: rgba(251, 251, 251, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: var(--text-color);
  border: 1px solid var(--accent-color);
  border-radius: 8px;
}
.arrow {
  font-size: 0.8rem;
}
.dropdown-menu {
  position: absolute;
  width: 100%;
  margin-top: 0.5rem;
  background: rgba(251, 251, 251, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(251, 251, 251, 0.1);
  border-radius: 8px;
  z-index: 100;
  max-height: 250px;
  overflow-y: auto;
}
ul {
  list-style: none;
  padding: 0.5rem;
  margin: 0;
}
li {
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-radius: 4px;
}
li:hover {
  background-color: rgba(197, 176, 205, 0.1); /* Faint accent color */
}
</style>