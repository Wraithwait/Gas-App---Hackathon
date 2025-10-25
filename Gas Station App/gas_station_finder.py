import tkinter as tk
from tkinter import ttk, messagebox
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import json
from typing import List, Dict, Tuple
import math

class GasStationFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Gas Station Finder")
        self.root.geometry("800x600")
        
        # User location
        self.user_lat = None
        self.user_lon = None
        
        # Gas station data (mock data for prototype)
        self.gas_stations = self.load_mock_data()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Gas Station Finder", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Location input section
        location_frame = ttk.LabelFrame(main_frame, text="Your Location", padding="10")
        location_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(location_frame, text="Enter your address:").grid(row=0, column=0, sticky=tk.W)
        self.address_entry = ttk.Entry(location_frame, width=50)
        self.address_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.get_location_btn = ttk.Button(location_frame, text="Get Location", command=self.get_user_location)
        self.get_location_btn.grid(row=1, column=1, padx=(10, 0))
        
        self.location_status = ttk.Label(location_frame, text="", foreground="red")
        self.location_status.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Search options section
        options_frame = ttk.LabelFrame(main_frame, text="Search Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Sort by option
        ttk.Label(options_frame, text="Sort by:").grid(row=0, column=0, sticky=tk.W)
        self.sort_var = tk.StringVar(value="closest")
        sort_combo = ttk.Combobox(options_frame, textvariable=self.sort_var, 
                                 values=["closest", "cheapest", "gas_type", "brand"], 
                                 state="readonly", width=15)
        sort_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Gas type filter
        ttk.Label(options_frame, text="Gas Type:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.gas_type_var = tk.StringVar(value="all")
        gas_type_combo = ttk.Combobox(options_frame, textvariable=self.gas_type_var,
                                     values=["all", "E85", "87", "89", "91"], 
                                     state="readonly", width=15)
        gas_type_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Brand filter
        ttk.Label(options_frame, text="Brand:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.brand_var = tk.StringVar(value="all")
        brand_combo = ttk.Combobox(options_frame, textvariable=self.brand_var,
                                  values=["all", "Shell", "Exxon", "BP", "Chevron", "Mobil", "Speedway", "7-Eleven"], 
                                  state="readonly", width=15)
        brand_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Search button
        self.search_btn = ttk.Button(options_frame, text="Find Gas Stations", command=self.search_gas_stations)
        self.search_btn.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create treeview for results
        columns = ("Station", "Brand", "Distance", "E85", "87", "89", "91")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100, anchor=tk.CENTER)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        location_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
    
    def load_mock_data(self) -> List[Dict]:
        """Load mock gas station data for prototype"""
        return [
            {
                "name": "Shell Station #1234",
                "brand": "Shell",
                "lat": 40.7128,
                "lon": -74.0060,
                "prices": {"E85": 2.89, "87": 3.45, "89": 3.65, "91": 3.85}
            },
            {
                "name": "Exxon Station #5678",
                "brand": "Exxon",
                "lat": 40.7589,
                "lon": -73.9851,
                "prices": {"E85": 2.95, "87": 3.52, "89": 3.72, "91": 3.92}
            },
            {
                "name": "BP Station #9012",
                "brand": "BP",
                "lat": 40.7505,
                "lon": -73.9934,
                "prices": {"E85": 2.82, "87": 3.38, "89": 3.58, "91": 3.78}
            },
            {
                "name": "Chevron Station #3456",
                "brand": "Chevron",
                "lat": 40.7614,
                "lon": -73.9776,
                "prices": {"E85": 2.91, "87": 3.48, "89": 3.68, "91": 3.88}
            },
            {
                "name": "Mobil Station #7890",
                "brand": "Mobil",
                "lat": 40.7505,
                "lon": -73.9934,
                "prices": {"E85": 2.87, "87": 3.44, "89": 3.64, "91": 3.84}
            },
            {
                "name": "Speedway Station #2468",
                "brand": "Speedway",
                "lat": 40.7282,
                "lon": -73.9942,
                "prices": {"E85": 2.79, "87": 3.35, "89": 3.55, "91": 3.75}
            },
            {
                "name": "7-Eleven Station #1357",
                "brand": "7-Eleven",
                "lat": 40.7505,
                "lon": -73.9934,
                "prices": {"E85": 2.85, "87": 3.41, "89": 3.61, "91": 3.81}
            }
        ]
    
    def get_user_location(self):
        """Get user's coordinates from address input"""
        address = self.address_entry.get().strip()
        if not address:
            self.location_status.config(text="Please enter an address", foreground="red")
            return
        
        try:
            geolocator = Nominatim(user_agent="gas_station_finder")
            location = geolocator.geocode(address)
            
            if location:
                self.user_lat = location.latitude
                self.user_lon = location.longitude
                self.location_status.config(text=f"Location found: {location.address}", foreground="green")
            else:
                self.location_status.config(text="Address not found. Please try a different address.", foreground="red")
                
        except Exception as e:
            self.location_status.config(text=f"Error getting location: {str(e)}", foreground="red")
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in miles"""
        return geodesic((lat1, lon1), (lat2, lon2)).miles
    
    def search_gas_stations(self):
        """Search and display gas stations based on criteria"""
        if not self.user_lat or not self.user_lon:
            messagebox.showerror("Error", "Please get your location first!")
            return
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Filter and calculate distances
        filtered_stations = []
        for station in self.gas_stations:
            # Apply brand filter
            if self.brand_var.get() != "all" and station["brand"] != self.brand_var.get():
                continue
            
            # Calculate distance
            distance = self.calculate_distance(
                self.user_lat, self.user_lon,
                station["lat"], station["lon"]
            )
            
            station["distance"] = distance
            filtered_stations.append(station)
        
        # Sort based on criteria
        sort_by = self.sort_var.get()
        if sort_by == "closest":
            filtered_stations.sort(key=lambda x: x["distance"])
        elif sort_by == "cheapest":
            # Sort by cheapest gas type (E85, 87, 89, 91 in order of preference)
            def get_cheapest_price(station):
                prices = station["prices"]
                # Return the minimum price available
                return min(prices.values())
            filtered_stations.sort(key=get_cheapest_price)
        elif sort_by == "gas_type":
            gas_type = self.gas_type_var.get()
            if gas_type != "all":
                filtered_stations.sort(key=lambda x: x["prices"].get(gas_type, float('inf')))
        elif sort_by == "brand":
            filtered_stations.sort(key=lambda x: x["brand"])
        
        # Display results
        for station in filtered_stations:
            prices = station["prices"]
            self.results_tree.insert("", "end", values=(
                station["name"],
                station["brand"],
                f"{station['distance']:.2f} mi",
                f"${prices.get('E85', 'N/A')}",
                f"${prices.get('87', 'N/A')}",
                f"${prices.get('89', 'N/A')}",
                f"${prices.get('91', 'N/A')}"
            ))

def main():
    root = tk.Tk()
    app = GasStationFinder(root)
    root.mainloop()

if __name__ == "__main__":
    main()




