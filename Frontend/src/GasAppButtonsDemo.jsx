import React, { useState } from "react";
import { motion } from "framer-motion";

export default function GasAppButtonsDemo() {
  const [active, setActive] = useState(false);

  return (
    <div className="min-h-screen grid place-items-center bg-gradient-to-b from-slate-50 to-slate-100 p-8">
      <div className="rounded-2xl bg-white p-8 shadow-lg max-w-md w-full text-center">
        <h1 className="text-2xl font-bold mb-4">Gas App – Button Test</h1>
        <p className="text-slate-600 mb-6">
          If this text looks styled, Tailwind is working ✅
        </p>

        {/* Button with press animation */}
        <motion.button
          whileTap={{ scale: 0.96 }}
          className="w-full mb-3 rounded-xl bg-emerald-600 text-white font-semibold py-3 shadow-lg hover:bg-emerald-500"
          onClick={() => alert("Pressed!")}
        >
          Press Me
        </motion.button>

        {/* Toggle Start/Stop */}
        <button
          onClick={() => setActive((a) => !a)}
          aria-pressed={active}
          className={`w-full rounded-xl font-semibold py-3 ring-1 ring-inset ${
            active
              ? "bg-amber-500 text-white ring-amber-600/40"
              : "bg-white text-slate-900 ring-slate-200 hover:bg-slate-50"
          }`}
        >
          {active ? "Stop" : "Start"}
        </button>
      </div>
    </div>
  );
}
