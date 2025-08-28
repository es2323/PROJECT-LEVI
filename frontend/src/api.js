import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// This code runs before every API request is sent.
apiClient.interceptors.request.use(
  (config) => {
    // Get the token from the browser's local storage.
    const token = localStorage.getItem('session_token');
    if (token) {
      // If the token exists, add it to the Authorization header.
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;