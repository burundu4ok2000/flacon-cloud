// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://burundu4ok2000.github.io',
  base: 'flacon-cloud',
  vite: {
    plugins: [tailwind()],
  },
});