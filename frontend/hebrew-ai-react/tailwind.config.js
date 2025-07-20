// Replace the content of tailwind.config.js with this:
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        hebrew: [
          'SBL Hebrew', 
          'Ezra SIL', 
          'David CLM',
          'Noto Sans Hebrew',
          'Arial Hebrew',
          'serif'
        ],
        sans: [
          'Inter',
          'ui-sans-serif', 
          'system-ui',
          'sans-serif'
        ],
      },
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}