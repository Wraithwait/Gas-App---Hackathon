module.exports = {
  content: ["./public/index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        fredoka: ['"Fredoka"', "sans-serif"],
        cinzel: ['"Cinzel"', "serif"], // <-- spooky header
      },
    },
  },
  plugins: [],
};
