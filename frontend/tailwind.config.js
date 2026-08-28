/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#eef2f8',
          100: '#d6e0ee',
          200: '#adc1dd',
          300: '#7f9dc8',
          400: '#4d74ab',
          500: '#2c5490',
          600: '#1c3f74',
          700: '#152f5a',
          800: '#0f2242',
          900: '#0a1830',
          950: '#060f1e',
        },
        saffron: {
          500: '#e08a2c',
          600: '#c8721a',
        },
        slate: {
          50: '#f7f8fa',
        },
      },
      fontFamily: {
        sans: ['"Inter"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
      boxShadow: {
        card: '0 1px 2px rgba(15, 34, 66, 0.06), 0 1px 3px rgba(15, 34, 66, 0.08)',
        cardHover: '0 4px 12px rgba(15, 34, 66, 0.10)',
      },
    },
  },
  plugins: [],
}
