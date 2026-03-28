/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'abyss-bg': '#0d0d0d',
        'abyss-panel': '#161616',
        'abyss-accent': '#ff3c00',
        'abyss-accent-hover': '#ff5e00',
        'abyss-text': '#e0e0e0',
        'abyss-green': '#32ff7e',
        'abyss-blue': '#7efff5',
      },
      fontFamily: {
        mono: ['Fira Code', 'Courier New', 'monospace'],
      }
    },
  },
  plugins: [],
}