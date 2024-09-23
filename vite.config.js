import { defineConfig } from 'vite';

export default defineConfig({
  base: '/evoslib/',
  root: './',
  build: {
    outDir: 'docs',
    rollupOptions: {
      input: 'index.html',
    },
  },
});