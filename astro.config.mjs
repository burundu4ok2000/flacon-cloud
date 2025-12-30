// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  vite: {
    plugins: [tailwind()],
    server: {
      proxy: {
        '/api': 'http://127.0.0.1:8000'
      }
    }
  },
});