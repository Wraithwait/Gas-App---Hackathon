import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Building2, Fuel, ChevronDown, ChevronUp } from "lucide-react";

/* ---------- Theme helpers ---------- */
const pumpkin = "bg-orange-500";
const pumpkinLight = "bg-orange-100";
const pumpkinText = "text-orange-800";

/* ---------- UI atoms ---------- */

const ToggleSwitch = ({ label, active, onToggle }) => (
  <div className="flex items-center justify-between py-2">
    <span className="text-slate-200">{label}</span>
    <button
      type="button"
      onClick={onToggle}
      className={`relative h-6 w-12 rounded-full transition-colors ${
        active ? pumpkin : "bg-slate-500"
      }`}
      aria-pressed={active}
    >
      <span
        className={`absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-all ${
          active ? "left-6" : "left-0.5"
        }`}
      />
    </button>
  </div>
);

const SelectableItem = ({ children, selected, onClick }) => (
  <button
    type="button"
    onClick={onClick}
    className={
      "w-full text-left rounded-md px-2 py-1 transition " +
      (selected
        ? `${pumpkinLight} ${pumpkinText} font-semibold`
        : "hover:bg-slate-700/40 text-slate-200")
    }
  >
    {children}
  </button>
);

/* ---------- Page ---------- */

export default function Dashboard() {
  // OPEN the sidebar on first load
  const [open, setOpen] = useState(true);
  // Keep sections CLOSED
  const [brandsOpen, setBrandsOpen] = useState(false);
  const [gasOpen, setGasOpen] = useState(false);
  // Pre-select Optimal
  const [sortMode, setSortMode] = useState("optimal");

  // Distance default 10 miles
  const [radiusMi, setRadiusMi] = useState(10);

  const [selectedBrand, setSelectedBrand] = useState(null);
  const [selectedFuel, setSelectedFuel] = useState(null);

  const SIDEBAR_W = 360;

  const brandList = [
    "Shell",
    "Arco",
    "Chevron",
    "Valero",
    "Sinclair",
    "76",
    "Mobil",
    "Circle K",
    "Gas",
    "Speedway Express",
    "Chevron G & M",
    "Chevron Extra Mile – G & M",
    "Chevron Extra Mile",
    "Speedway",
    "G & M Oil",
    "G & M Food Mart",
    "AM/PM",
    "Costco Gas Station",
  ];

  const fuelOptions = [
    "Regular: 87",
    "Midgrade: 89",
    "Premium: 91",
    "Ethanol: E85",
  ];

  const openTransition = { type: "tween", duration: 0.55, ease: [0.16, 1, 0.3, 1] };
  const closeTransition = { type: "tween", duration: 0.45, ease: [0.16, 1, 0.3, 1] };

  return (
    <div className="min-h-screen bg-[radial-gradient(90%_120%_at_50%_-10%,#1f2937_0%,#0b1220_70%)] text-white">
      {/* Top bar */}
      <header className="flex h-16 items-center border-b border-white/10 bg-slate-900/40 backdrop-blur">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4">
          <img src="/home_page/newlogo.png" alt="Friendly Fumes" className="h-10 w-auto" />
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">
        <section className="relative overflow-hidden rounded-2xl bg-slate-900/60 ring-1 ring-white/10 shadow-xl">
          {/* Filters pill */}
          <button
            onClick={() => setOpen((o) => !o)}
            type="button"
            aria-expanded={open}
            className={
              "absolute left-4 top-3 z-30 rounded-full px-4 py-1 text-sm font-semibold shadow-sm ring-2 transition " +
              (open
                ? "bg-gray-300 text-gray-800 ring-gray-300 hover:bg-gray-400"
                : "bg-gray-600 text-white ring-gray-600/30 hover:bg-gray-700")
            }
          >
            Filters
          </button>

          <div className="relative min-h-[76vh]">
            {/* Sidebar */}
            <AnimatePresence initial={false}>
              {open && (
                <motion.aside
                  key="filters"
                  initial={{ x: -16, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: -16, opacity: 0 }}
                  transition={open ? openTransition : closeTransition}
                  className="absolute left-0 top-0 z-20 h-full w-[360px] border-r border-white/10 bg-slate-900/80 p-4 pt-12"
                >
                  {/* BRANDS (collapsed by default) */}
                  <div className="mb-4">
                    <button
                      type="button"
                      onClick={() => setBrandsOpen((b) => !b)}
                      className={
                        "flex w-full items-center justify-between rounded-lg px-2 py-2 font-semibold transition " +
                        (brandsOpen
                          ? "bg-gray-100 text-gray-800 ring-1 ring-gray-200"
                          : "text-slate-200 hover:bg-slate-800/60")
                      }
                    >
                      <span className="flex items-center gap-2">
                        <Building2 className="h-4 w-4" />
                        Brands
                      </span>
                      {brandsOpen ? <ChevronUp /> : <ChevronDown />}
                    </button>

                    <AnimatePresence initial={false}>
                      {brandsOpen && (
                        <motion.div
                          key="brands-body"
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.25 }}
                          className="pt-2 pl-2"
                        >
                          <div className="max-h-60 space-y-1 overflow-auto pr-1">
                            {brandList.map((b) => (
                              <SelectableItem
                                key={b}
                                selected={selectedBrand === b}
                                onClick={() =>
                                  setSelectedBrand((cur) => (cur === b ? null : b))
                                }
                              >
                                • {b}
                              </SelectableItem>
                            ))}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* GAS TYPE (collapsed by default) */}
                  <div className="mb-4">
                    <button
                      type="button"
                      onClick={() => setGasOpen((g) => !g)}
                      className={
                        "flex w-full items-center justify-between rounded-lg px-2 py-2 font-semibold transition " +
                        (gasOpen
                          ? "bg-gray-100 text-gray-800 ring-1 ring-gray-200"
                          : "text-slate-200 hover:bg-slate-800/60")
                      }
                    >
                      <span className="flex items-center gap-2">
                        <Fuel className="h-4 w-4" />
                        Gas Type
                      </span>
                      {gasOpen ? <ChevronUp /> : <ChevronDown />}
                    </button>

                    <AnimatePresence initial={false}>
                      {gasOpen && (
                        <motion.div
                          key="gas-body"
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.25 }}
                          className="pl-2 pt-2"
                        >
                          <div className="space-y-1">
                            {["Regular: 87", "Midgrade: 89", "Premium: 91", "Ethanol: E85"].map(
                              (label) => (
                                <SelectableItem
                                  key={label}
                                  selected={selectedFuel === label}
                                  onClick={() =>
                                    setSelectedFuel((cur) => (cur === label ? null : label))
                                  }
                                >
                                  {label}
                                </SelectableItem>
                              )
                            )}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* DISTANCE (stays at 10 by default) */}
                  <div className="mb-4">
                    <div className="mb-1 text-sm font-semibold text-slate-200">
                      Distance
                    </div>
                    <div className="flex items-center justify-between text-sm text-slate-300">
                      <span>0 mi</span>
                      <span className="font-medium text-white">{radiusMi} mi</span>
                      <span>30 mi</span>
                    </div>
                    <input
                      type="range"
                      min={1}
                      max={30}
                      value={radiusMi}
                      onChange={(e) => setRadiusMi(Number(e.target.value))}
                      className="mt-2 w-full accent-orange-500"
                    />
                  </div>

                  {/* Toggles (Optimal pre-checked) */}
                  <div className="border-t border-white/10 pt-3">
                    <ToggleSwitch
                      label="Closest"
                      active={sortMode === "closest"}
                      onToggle={() =>
                        setSortMode((m) => (m === "closest" ? null : "closest"))
                      }
                    />
                    <ToggleSwitch
                      label="Cheapest"
                      active={sortMode === "cheapest"}
                      onToggle={() =>
                        setSortMode((m) => (m === "cheapest" ? null : "cheapest"))
                      }
                    />
                    <ToggleSwitch
                      label="Optimal"
                      active={sortMode === "optimal"}
                      onToggle={() =>
                        setSortMode((m) => (m === "optimal" ? null : "optimal"))
                      }
                    />
                  </div>
                </motion.aside>
              )}
            </AnimatePresence>

            {/* Content */}
            <motion.div
              className="relative p-3"
              animate={{ x: open ? SIDEBAR_W : 0 }}
              transition={open ? openTransition : closeTransition}
            >
              <div className="mb-3 text-center text-sm font-semibold text-slate-200">
                Nearby Gas Stations
              </div>

              <motion.div
                layout
                className="grid grid-cols-1 gap-3 md:grid-cols-[1fr_340px]"
              >
                {/* Map */}
                <div className="grid h-[70vh] place-items-center rounded-2xl border border-white/10 bg-slate-800 text-slate-200">
                  Map goes here
                </div>

                {/* Results */}
                <div className="rounded-2xl border border-white/10 bg-slate-900/40 p-3">
                  <div className="mb-2 flex items-center justify-between text-sm font-semibold text-slate-200">
                    <span>Results</span>
                    <div className="flex flex-wrap items-center gap-2">
                      {selectedBrand && (
                        <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs font-medium text-slate-100">
                          {selectedBrand}
                        </span>
                      )}
                      {selectedFuel && (
                        <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs font-medium text-slate-100">
                          {selectedFuel}
                        </span>
                      )}
                      {sortMode && (
                        <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs font-medium text-slate-100">
                          {sortMode.charAt(0).toUpperCase() + sortMode.slice(1)}
                        </span>
                      )}
                      <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs font-medium text-slate-100">
                        {radiusMi} mi
                      </span>
                    </div>
                  </div>

                  <div className="text-sm text-slate-300">
                    No stations found in this radius.
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </section>
      </main>
    </div>
  );
}
