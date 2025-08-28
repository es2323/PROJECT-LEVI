import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // This tells Vite to forward any request that starts with /api
      // to your backend server running on port 8000.
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})