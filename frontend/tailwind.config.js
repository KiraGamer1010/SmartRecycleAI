/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        graphite: "#07100f",
        graphiteSoft: "#0a1514",
        panel: "#0d1b19",
        panelSoft: "#122421",
        mint: "#52f2a8",
        algae: "#0fbf84",
        solar: "#f7c948",
        signal: "#38bdf8",
        frost: "#ecfdf5",
        ink: "#03100d"
      },
      boxShadow: {
        glow: "0 0 28px rgba(82, 242, 168, 0.18)",
        premium: "0 24px 80px rgba(0, 0, 0, 0.28)"
      },
      backgroundImage: {
        "premium-grid":
          "linear-gradient(rgba(82, 242, 168, 0.055) 1px, transparent 1px), linear-gradient(90deg, rgba(56, 189, 248, 0.045) 1px, transparent 1px)",
        "scanner-radial":
          "radial-gradient(circle at 22% 18%, rgba(82, 242, 168, 0.18), transparent 34%), radial-gradient(circle at 82% 12%, rgba(56, 189, 248, 0.12), transparent 30%)"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" }
        }
      },
      animation: {
        float: "float 6s ease-in-out infinite"
      }
    }
  },
  plugins: []
};
