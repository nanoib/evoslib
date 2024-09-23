import { defineConfig } from 'vite';

export default defineConfig({
  base: '/evoslib/',
  root: './',
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: 'index.html',
    },
  },
});