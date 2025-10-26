import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Landing() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-black text-white">
      {/* Logo */}
      <img
        src="/home_page/Home_page_logo.png"
        alt="Friendly Fumes"
        className="absolute left-6 top-6 w-[240px] max-w-[70vw] select-none"
        draggable="false"
      />

      {/* 🕸️ Bottom-left web */}
<img
  src="/home_page/web.png"
  alt=""
  className="pointer-events-none absolute -left-[200px] -bottom-[150px] w-[600px] opacity-40 filter grayscale"
  draggable="false"
/>

{/* 🕸️ Bottom-right web */}
<img
  src="/home_page/web.png"
  alt=""
  className="pointer-events-none absolute -right-[200px] -bottom-[150px] w-[600px] opacity-40 filter grayscale"
  draggable="false"
/>

{/* 🕸️ Top-right web */}
<img
  src="/home_page/web.png"
  alt=""
  className="pointer-events-none absolute -right-[180px] -top-[140px] w-[520px] opacity-40 filter grayscale"
  draggable="false"
/>

      {/* Center text */}
      <main className="relative mx-auto grid min-h-screen max-w-5xl place-items-start px-6 pt-24 md:pt-28">
        <div className="z-10 w-full text-center">
          <h1 className="mb-4 font-serif text-5xl font-extrabold tracking-tight md:text-6xl lg:text-7xl">
            Find the best gas for you!
          </h1>
          <p className="mx-auto mb-8 max-w-3xl text-lg text-slate-200 md:text-xl lg:text-2xl">
            Whether your in a rush or on a budget we have the right station for you.
          </p>

          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.97 }}
            transition={{ type: "spring", stiffness: 300, damping: 20 }}
            className="inline-block"
          >
            <Link
              to="/dashboard"
              className="inline-block rounded-[999px] bg-[#2b1a14] px-10 py-4 text-lg font-semibold text-white shadow-[0_6px_0_rgba(0,0,0,0.35)] ring-1 ring-white/10 hover:bg-[#3a241c] focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-400"
            >
              Next!
            </Link>
          </motion.div>
        </div>
      </main>

      {/* Pumpkin - bottom left corner */}
      <img
        src="/home_page/pumpkin.png"
        alt=""
        aria-hidden="true"
        className="pointer-events-none absolute left-20 bottom-2 w-48 md:w-60 select-none"
        draggable="false"
      />

      {/* 🛢️ Gas can - bottom right corner */}
<div className="pointer-events-none absolute right-[120px] -bottom-[50px] select-none md:right-[280px]">
  <img
    src="/home_page/gas.png"
    alt="Gas Can"
    className="relative z-40 w-[360px] md:w-[370px]"
    draggable="false"
  />

        {/* Spark top-left of gas can */}
        <img
          src="/home_page/pumking_spark.png"
          alt=""
          aria-hidden="true"
          className="absolute -top-10 -left-8 w-14 rotate-[-10deg] md:w-16"
          draggable="false"
        />
      </div>
    </div>
  );
}
