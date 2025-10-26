import React, { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Building2, Fuel, ChevronDown, ChevronUp, MapPin } from "lucide-react";
import Map, { Marker, Popup } from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css";

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
  // Sidebar open on first load (unchanged)
  const [open, setOpen] = useState(true);

  // Sections COLLAPSED on first load (but defaults are already selected)
  const [brandsOpen, setBrandsOpen] = useState(false);
  const [gasOpen, setGasOpen] = useState(false);

  // Sort: default to "cheapest", "optimal" removed
  const [sortMode, setSortMode] = useState("closest");

  // Distance default 10 miles
  const [radiusMi, setRadiusMi] = useState(10);

  // Single-select with "All" sentinel; both pre-selected to "All"
  const [selectedBrand, setSelectedBrand] = useState(null);
  const [selectedFuel, setSelectedFuel] = useState(null);

  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mapboxToken, setMapboxToken] = useState(null);
  const [userLocation, setUserLocation] = useState(null);
  const [popupInfo, setPopupInfo] = useState(null);

  const SIDEBAR_W = 360;
  const brandList = [ "Shell", "Arco",
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

  // Added "Diesel"
  const fuelOptions = ["Regular: 87", "Midgrade: 89", "Premium: 91", "Ethanol: E85", "Diesel"];

  const openTransition = { type: "tween", duration: 0.55, ease: [0.16, 1, 0.3, 1] }; 
  const closeTransition = { type: "tween", duration: 0.45, ease: [0.16, 1, 0.3, 1] }; 

  useEffect(() => {
    setMapboxToken('pk.eyJ1Ijoid3JhaXRod2FpdCIsImEiOiJjbWg2cHRiajgwa3N0MmpvbW9mZ2lxeGtqIn0.UXl2DSFjbSSRntzofhFm9g');
  }, []);

  // Get user's location on component mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
        },
        (error) => {
          console.error("Error getting user location:", error);
          // Fallback to default location if permission is denied or an error occurs
          setUserLocation({ latitude: 33.6846, longitude: -117.9262 });
        }
      );
    } else {
      console.error("Geolocation is not supported by this browser.");
      // Fallback for older browsers
      setUserLocation({ latitude: 33.6846, longitude: -117.9262 });
    }
  }, []); // Empty dependency array ensures this runs only once

  const fetchStations = useCallback(async () => {
    // Do not fetch if location is not yet available.
    if (!userLocation) {
      return;
    }

    setLoading(true);
    setPopupInfo(null); // Close popup on new search

    let gas_type = "all"; 
    if (selectedFuel) {
      if (selectedFuel.includes("87")) gas_type = "87";
      else if (selectedFuel.includes("89")) gas_type = "89";
      else if (selectedFuel.includes("91")) gas_type = "91";
      else if (selectedFuel.toLowerCase().includes("e85")) gas_type = "E85";
      else if (selectedFuel.toLowerCase().includes("diesel")) gas_type = "diesel";
    }

    const searchParams = {
      lat: userLocation?.latitude,
      lon: userLocation?.longitude,
      radius: radiusMi,
      gas_type: gas_type,
      brand: selectedBrand || "all",
      sort_by: sortMode,
    };

    try {
      const response = await fetch(`http://127.0.0.1:5000/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchParams),
      });
      const data = await response.json();
      setStations(data.results || []);
    } catch (error) {
      console.error("Failed to fetch stations:", error);
      setStations([]);
    } finally {
      setLoading(false);
    }
  }, [radiusMi, selectedBrand, selectedFuel, sortMode, userLocation]);

  useEffect(() => {
    // Fetch stations whenever filters change
    if (userLocation) {
      fetchStations();
    } 
  }, [userLocation, fetchStations]);

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
                  {/* BRANDS (collapsed by default; 'All' is pre-selected) */}
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
                            {/* ALL option, pre-selected */}
                            <SelectableItem
                              selected={selectedBrand === null}
                              onClick={() => setSelectedBrand(null)}
                            >
                              All
                            </SelectableItem>

                            {brandList.map((b) => (
                              <SelectableItem
                                key={b}
                                selected={selectedBrand === b}
                                onClick={() => setSelectedBrand(b)}
                              >
                                {b}
                              </SelectableItem>
                            ))}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* GAS TYPE (collapsed by default; 'All' is pre-selected) */}
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
                            {/* ALL option, pre-selected */}
                            <SelectableItem
                              selected={selectedFuel === null}
                              onClick={() => setSelectedFuel(null)}
                            >
                              All
                            </SelectableItem>

                            {fuelOptions.map((label) => (
                              <SelectableItem
                                key={label}
                                selected={selectedFuel === label}
                                onClick={() => setSelectedFuel(label)}
                              >
                                {label}
                              </SelectableItem>
                            ))}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* DISTANCE (10 mi default) */}
                  <div className="mb-4">
                    <div className="mb-1 text-sm font-semibold text-slate-200">Distance</div>
                    <div className="flex items-center justify-between text-sm text-slate-300">
                      <span>0 mi</span>
                      <span className="font-medium text-white">{radiusMi} mi</span>
                      <span>10 mi</span>
                    </div>
                    <input
                      type="range"
                      min={1}
                      max={10}
                      value={radiusMi}
                      onChange={(e) => setRadiusMi(Number(e.target.value))}
                      className="mt-2 w-full accent-orange-500"
                    />
                  </div>

                  {/* Sort toggles (Cheapest pre-checked, Optimal removed) */}
                  <div className="border-t border-white/10 pt-3">
                    <ToggleSwitch
                      label="Closest"
                      active={sortMode === "closest"}
                      onToggle={() => setSortMode("closest")}
                    />
                    <ToggleSwitch
                      label="Cheapest"
                      active={sortMode === "cheapest"}
                      onToggle={() => setSortMode("cheapest")}
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
                <div className="h-[70vh] rounded-2xl border border-white/10 bg-slate-800 text-slate-200 overflow-hidden">
                  {mapboxToken && userLocation ? (
                    <Map
                      key={userLocation.latitude} // Re-mount map when location changes
                      initialViewState={{
                        ...userLocation,
                        zoom: 12,
                      }}
                      mapboxAccessToken={mapboxToken}
                      mapStyle="mapbox://styles/mapbox/dark-v11"
                      style={{ width: "100%", height: "100%" }}
                    >
                      {/* Marker for User's Location */}
                      <Marker latitude={userLocation.latitude} longitude={userLocation.longitude}>
                        <div className="h-4 w-4 rounded-full bg-blue-500 border-2 border-white" />
                      </Marker>

                      {stations.map((station, index) => (
                        <Marker
                          key={station.name + station.address}
                          latitude={station.lat}
                          longitude={station.lon}
                          onClick={(e) => {
                            e.originalEvent.stopPropagation();
                            setPopupInfo(station);
                          }}
                        >
                          <MapPin className="h-6 w-6 text-orange-500 cursor-pointer" />
                        </Marker>
                      ))}

                      {popupInfo && (
                        <Popup
                          anchor="top"
                          latitude={popupInfo.lat}
                          longitude={popupInfo.lon}
                          onClose={() => setPopupInfo(null)}
                          closeOnClick={false}
                        >
                          <div className="text-sm text-black">
                            <div className="font-bold">{popupInfo.name}</div>
                            <div>{popupInfo.address}</div>
                            <div><strong>Distance:</strong> {popupInfo.distance_miles} mi</div>
                          </div>
                        </Popup>
                      )}
                    </Map>
                  ) : (
                    <div className="flex h-full items-center justify-center">Loading Map...</div>
                  )}
                </div>

                {/* Results */}
                <div className="rounded-2xl border border-white/10 bg-slate-900/40 p-3">
                  <div className="mb-2 flex items-center justify-between text-sm font-semibold text-slate-200">
                    <span>Results</span>
                  </div>

                  {loading ? (
                    <div className="text-center text-slate-300">Loading...</div>
                  ) : stations.length === 0 ? (
                    <div className="text-center text-slate-300">No stations found.</div>
                  ) : (
                    <ul className="h-[65vh] space-y-2 overflow-y-auto pr-1">
                      {stations.map((s) => (
                        <li key={s.name + s.address} className="cursor-pointer rounded bg-slate-800 px-3 py-2 text-sm transition-colors hover:bg-slate-700/80" onClick={() => setPopupInfo(s)}>
                          <div className="font-semibold text-white">{s.name}</div>
                          <div className="text-xs text-slate-400">{s.address}</div>
                          <div className="text-xs text-slate-400">Distance: {s.distance_miles} mi</div>
                          <div className="mt-1 text-xs font-medium text-green-300">
                            {(() => {
                              if (Object.keys(s.prices).length === 0) {
                                return "Prices not available";
                              }

                              let priceKey = '87'; // Default to regular
                              let displayLabel = '87';

                              if (selectedFuel) {
                                if (selectedFuel.includes(':')) {
                                  priceKey = selectedFuel.split(': ')[1];
                                  displayLabel = priceKey;
                                } else if (selectedFuel.toLowerCase() === 'diesel') {
                                  priceKey = 'diesel';
                                  displayLabel = 'Diesel';
                                }
                              }
                              return s.prices[priceKey] ? `${displayLabel}: $${s.prices[priceKey].toFixed(2)}` : `87: $${s.prices['87']?.toFixed(2) || 'N/A'}`;
                            })()}
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </motion.div>
            </motion.div>
          </div>
        </section>
      </main>
    </div>
  );
}
