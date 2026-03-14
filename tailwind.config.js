/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        parchment: { DEFAULT: '#f9f5eb', alt: '#f1e8d3' },
        'book-border': '#d8c8a4',
        ink: '#1e1609',
        muted: '#6b5438',
        accent: '#7a1a1a',
        gold: '#9a7010',
        sidebar: {
          DEFAULT: '#17110a',
          text: '#e8d4b0',
          accent: '#c8980e',
          link: '#b09060',
        },
      },
      fontFamily: {
        serif: ['"EB Garamond"', 'Georgia', '"Times New Roman"', 'serif'],
        arabic: ['"Amiri"', 'serif'],
      },
    },
  },
  plugins: [],
}
