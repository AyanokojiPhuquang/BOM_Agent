import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  server: {
    allowedHosts: ['starlink.yitec.dev'],
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8030',
        changeOrigin: true,
      },
    },
  },
})
