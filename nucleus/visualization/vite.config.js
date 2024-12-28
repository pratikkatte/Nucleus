import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        format: 'es', // Ensure the format is set to 'es'
      },
    },
  },
  worker: {
    format: 'es', // Use 'es' for workers
  },
})
