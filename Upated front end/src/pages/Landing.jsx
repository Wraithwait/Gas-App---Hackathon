// src/pages/Landing.jsx
import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

/* ================================
   🔧 QUICK TWEAK KNOBS (easy to edit)
   ================================ */
const HERO_OFFSET_PX = 280; // push title/subtitle/button lower (increase to move down)

// Neon styles
const NEON_ORANGE_TITLE = `
  0 0 5px #ffb347,
  0 0 10px #ffb347,
  0 0 20px #ff8c00,
  0 0 40px #ff8c00,
  0 0 80px #ff6600
`;
const NEON_WHITE_TEXT = `
  0 0 6px #ffffff,
  0 0 12px #cccccc,
  0 0 20px rgba(255,255,255,0.7)
`;
const NEON_BROWN_BUTTON_GLOW = `
  0 0 10px rgba(123, 74, 46, 0.9),
  0 0 16px rgba(160, 98, 62, 0.9),
  0 0 26px rgba(199, 130, 84, 0.85)
`;

// Button classes + inline style for the brown neon
const BUTTON_CLASSES = [
  "inline-block",
  "rounded-[999px]",
  "px-12",
  "py-5",
  "text-lg",
  "font-semibold",
  "text-white",
  "transition-all",
  "duration-300",
  "ease-in-out",
  "focus:outline-none",
  "focus-visible:ring-4",
  "focus-visible:ring-orange-300",
].join(" ");

const BUTTON_STYLE = {
  // Brown gradient base
  background: "linear-gradient(180deg, #8b5a3a 0%, #5c3a25 100%)",
  // Outer neon glow (brown/orange family)
  boxShadow: NEON_BROWN_BUTTON_GLOW,
  // Crisp edge
  border: "2px solid rgba(199,130,84,0.6)",
  // Slight inner glow via text shadow
  textShadow: "0 0 6px rgba(255,255,255,0.35)",
};

/* ================================
   🧩 COMPONENT
   ================================ */
export default function Landing() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-black text-white">
      {/* =========================
          Logo (top-left, fixed size)
         ========================= */}
      <img
        src="/home_page/Home_page_logo.png"
        alt="Friendly Fumes"
        className="absolute left-6 top-6 w-[240px] max-w-[70vw] select-none"
        draggable="false"
      />

      {/* =========================
          Webs (decor)
         ========================= */}
      {/* Bottom-left web — your corner file, bright & visible */}
      <img
        src="/home_page/left_down_web.png"
        alt="Left Corner Web"
        className="pointer-events-none absolute left-[-24px] bottom-[-52px] w-[600px] opacity-100"
        draggable="false"
      />

      {/* Bottom-right web — keep your original generic web */}
      <img
        src="/home_page/web.png"
        alt="Bottom Right Web"
        className="pointer-events-none absolute -right-[200px] -bottom-[150px] w-[600px] opacity-90"
        draggable="false"
      />

      {/* Top-right web — your smiling spider file, keep natural color + soft drop shadow */}
      <img
        src="/home_page/right_up_web.png"
        alt="Top Right Spider Web"
        className="pointer-events-none absolute right-0 top-0 z-10 w-[420px] select-none drop-shadow-[0_0_6px_rgba(255,255,255,0.35)]"
        draggable="false"
      />

      {/* =========================
          Sparkles (easy to move)
         ========================= */}
      {[
        { left: "10%", top: "25%", size: "150px", opacity: 1 },
        { right: "17%", top: "40%", size: "140px", opacity: 0.1 },
        { left: "25%", bottom: "35%", size: "110px", opacity: 0.1 },
        { right: "40%", top: "10%", size: "120px", opacity: 1 },
        { left: "38%", bottom: "15%", size: "110px", opacity: 1 },
      ].map((s, i) => (
        <img
          key={i}
          src="/home_page/sparkles.png"
          alt={`Sparkle ${i + 1}`}
          className="absolute animate-pulse pointer-events-none select-none"
          style={{
            left: s.left,
            right: s.right,
            top: s.top,
            bottom: s.bottom,
            width: s.size,
            opacity: s.opacity,
          }}
          draggable="false"
        />
      ))}

      {/* =========================
          Hero (title + subtitle + button)
         ========================= */}
      <main
        className="relative mx-auto grid min-h-screen max-w-5xl place-items-start px-6"
        style={{ paddingTop: `${HERO_OFFSET_PX}px` }}
      >
        <div className="z-10 w-full text-center">
          {/* Neon orange title */}
          <h1
            className="mb-4 font-serif font-extrabold tracking-tight text-6xl md:text-6xl lg:text-7xl"
            style={{
              color: "#ffb347",
              textShadow: NEON_ORANGE_TITLE,
            }}
          >
            Find the best gas for you!
          </h1>

          {/* Neon white subtitle (brighter & crisper) */}
          <p
            className="mx-auto mb-8 max-w-3xl text-lg md:text-2xl lg:text-3xl"
            style={{
              color: "#ffffff",
              textShadow: NEON_WHITE_TEXT,
            }}
          >
            Whether you're in a rush or on a budget, we have the right station for you.
          </p>

          {/* Brown neon "Next!" button (eye-catchy) */}
          <motion.div
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.95 }}
            transition={{ type: "spring", stiffness: 300, damping: 18 }}
            className="inline-block"
          >
            <Link to="/dashboard" className={BUTTON_CLASSES} style={BUTTON_STYLE}>
              Next!
            </Link>
          </motion.div>
        </div>
      </main>

      {/* =========================
          Pumpkin (movable & larger)
         ========================= */}
      <img
        src="/home_page/pumpkin.png"
        alt="Pumpkin"
        aria-hidden="true"
        className="pointer-events-none absolute select-none"
        style={{
          // You can change any of these 4 values to reposition easily
          left: "340px",
          right: "60px",
          bottom: "-40px",
          width: "300px",
          maxWidth: "none",
        }}
        draggable="false"
      />

      {/* =========================
          Gas can + spark (right-bottom)
         ========================= */}
      <div className="pointer-events-none absolute select-none right-[120px] -bottom-[50px] md:right-[280px]">
        <img
          src="/home_page/gas.png"
          alt="Gas Can"
          className="relative z-40 w-[360px] md:w-[370px]"
          draggable="false"
        />
        {/* Spark near gas (top-left of can). Adjust -top/-left to fine-tune */}
        <img
          src="/home_page/pumking_spark.png"
          alt="Pumpkin Spark"
          className="absolute -top-2 -left-6 w-36 rotate-[-8deg] md:w-18"
          draggable="false"
        />
      </div>
    </div>
  );
}
