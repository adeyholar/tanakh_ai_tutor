import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      allow: [
        'D:/AI/Gits/tanakh_ai_tutor/frontend/hebrew-ai-react',
        'D:/AI/Gits/tanakh_ai_tutor/frontend/hebrew-ai-react/node_modules',
      ],
    },
  },
});