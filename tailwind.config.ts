import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        hijau: {
          utama: "#86A889",
          hover: "#6F9172",
          muda: "#DCEBDD",
          soft: "#F3F8F3",
        },
        kuning: {
          muda: "#F7E7A8",
          soft: "#FFF9DF",
          aksen: "#E6CA65",
        },
        teks: {
          utama: "#26352A",
          sekunder: "#68756C",
          muted: "#94A3B8",
        },
        latar: {
          soft: "#F8FAF8",
        }
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
      }
    },
  },
  plugins: [],
};
export default config;
