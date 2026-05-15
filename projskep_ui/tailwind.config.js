/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0a0a0c",
        panel: "rgba(20, 20, 25, 0.7)",
        accent: "#00d2ff",
        warning: "#ffaa00",
        risk: "#ff4444",
        glow: "rgba(0, 210, 255, 0.1)",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      boxShadow: {
        'glow': '0 0 15px rgba(0, 210, 255, 0.2)',
      }
    },
  },
  plugins: [],
}
