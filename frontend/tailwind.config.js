/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        graphite: "#07100f",
        panel: "#0d1b19",
        mint: "#52f2a8",
        algae: "#0fbf84",
        solar: "#f7c948",
        signal: "#38bdf8"
      },
      boxShadow: {
        glow: "0 0 28px rgba(82, 242, 168, 0.18)"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
};
