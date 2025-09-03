// frontend/src/composables/useAuth.js
import { ref, computed } from 'vue';

// This state is shared across the entire app
const user = ref(null);

export function useAuth() {
  const isAuthenticated = computed(() => !!user.value);

  // A function to simulate logging in with mock data
  function login() {
    user.value = {
      name: 'Enosh Earnest',
      email: 'enosh.earnest@example.com',
      picture: 'https://path.to/your/profile/pic.jpg' // Optional
    };
  }

  // A function to simulate logging out
  function logout() {
    user.value = null;
  }

  return {
    user,
    isAuthenticated,
    login,
    logout,
  };
}