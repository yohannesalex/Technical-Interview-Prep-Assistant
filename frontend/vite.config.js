import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Vite configuration for React development server
 *
 * - Enables React support (JSX, Fast Refresh)
 * - Runs the development server on port 5173
 * - Proxies `/api` requests to the backend server at http://localhost:8000
 *   to prevent CORS issues during local development
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
