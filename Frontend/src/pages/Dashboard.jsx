import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Building2, Fuel, ChevronDown, ChevronUp } from "lucide-react";
import { useEffect } from "react";

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
  const [open, setOpen] = useState(true);
  const [brandsOpen, setBrandsOpen] = useState(false);
  const [gasOpen, setGasOpen] = useState(false);
  const [sortMode, setSortMode] = useState("optimal");
  const [radiusMi, setRadiusMi] = useState(10);
  const [selectedBrand, setSelectedBrand] = useState(null);
  const [selectedFuel, setSelectedFuel] = useState(null);

  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(false);
  const SIDEBAR_W = 360;
  const openTransition = { type: "tween", duration: 0.55, ease: [0.16, 1, 0.3, 1] };
  const closeTransition = { type: "tween", duration: 0.45, ease: [0.16, 1, 0.3, 1] };

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
	
  useEffect(() => {
	  fetchStations();
  }, [selectedFuel, selectedBrand, sortMode]);

  async function fetchStations() {
    setLoading(true);
    let grade = "default";
    if (selectedFuel) {
      if (selectedFuel.includes("87")) grade = "regular";
      else if (selectedFuel.includes("89")) grade = "midgrade";
      else if (selectedFuel.includes("91")) grade = "premium";
      else if (selectedFuel.toLowerCase().includes("e85")) grade = "e85";
    }

	const params = new URLSearchParams({
	  grade,
	  brand: selectedBrand || "Default",
	  sort: sortMode || "Defaullt",
	});

	const response = await fetch('http://127.0.0.1:5000/?${params.toString()}');
	const data = await response.json();
	setStations(data);
	setLoading(false);
  }

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
          {/* Filters button */}
          <button
            onClick={() => setOpen((o) => !o)}
            type="button"
            className={`absolute left-4 top-3 z-30 rounded-full px-4 py-1 text-sm font-semibold shadow-sm ring-2 transition ${
              open
                ? "bg-gray-300 text-gray-800 ring-gray-300 hover:bg-gray-400"
                : "bg-gray-600 text-white ring-gray-600/30 hover:bg-gray-700"
            }`}
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
                  {/* BRAND selector */}
                  <div className="mb-4">
                    <button
                      type="button"
                      onClick={() => setBrandsOpen((b) => !b)}
                      className={`flex w-full items-center justify-between rounded-lg px-2 py-2 font-semibold transition ${
                        brandsOpen
                          ? "bg-gray-100 text-gray-800 ring-1 ring-gray-200"
                          : "text-slate-200 hover:bg-slate-800/60"
                      }`}
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

                  {/* GAS TYPE selector */}
                  <div className="mb-4">
                    <button
                      type="button"
                      onClick={() => setGasOpen((g) => !g)}
                      className={`flex w-full items-center justify-between rounded-lg px-2 py-2 font-semibold transition ${
                        gasOpen
                          ? "bg-gray-100 text-gray-800 ring-1 ring-gray-200"
                          : "text-slate-200 hover:bg-slate-800/60"
                      }`}
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
                            {fuelOptions.map((label) => (
                              <SelectableItem
                                key={label}
                                selected={selectedFuel === label}
                                onClick={() =>
                                  setSelectedFuel((cur) => (cur === label ? null : label))
                                }
                              >
                                {label}
                              </SelectableItem>
                            ))}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* TOGGLES */}
                  <div className="border-t border-white/10 pt-3">
                    <ToggleSwitch
                      label="Closest"
                      active={sortMode === "shortest"}
                      onToggle={() => setSortMode("shortest")}
                    />
                    <ToggleSwitch
                      label="Cheapest"
                      active={sortMode === "cheapest"}
                      onToggle={() => setSortMode("cheapest")}
                    />
                    <ToggleSwitch
                      label="Optimal"
                      active={sortMode === "optimal"}
                      onToggle={() => setSortMode("optimal")}
                    />
                  </div>
                </motion.aside>
              )}
            </AnimatePresence>

            {/* RESULTS */}
            <motion.div
              className="relative p-3"
              animate={{ x: open ? SIDEBAR_W : 0 }}
              transition={open ? openTransition : closeTransition}
            >
              <div className="mb-3 text-center text-sm font-semibold text-slate-200">
                Nearby Gas Stations
              </div>

              <div className="rounded-2xl border border-white/10 bg-slate-900/40 p-3 text-sm text-slate-300">
                {loading ? (
                  <div>Loading...</div>
                ) : stations.length === 0 ? (
                  <div>No stations found.</div>
                ) : (
                  <ul className="space-y-2">
                    {stations.map((s, i) => (
                      <li key={i} className="rounded bg-slate-800 px-3 py-2">
                        <div className="font-semibold text-white">{s.brand_name}</div>
                        <div className="text-slate-400 text-xs">
                          Address: {s.address || "N/A"}
                        </div>
                        <div className="text-slate-400 text-xs">
                          Prices:{" "}
                          {Object.entries(s.prices)
                            .map(([k, v]) => `${k}: ${v ?? "N/A"}`)
                            .join(", ")}
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </motion.div>
          </div>
        </section>
      </main>
    </div>
  );
}
