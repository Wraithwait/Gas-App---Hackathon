#!/usr/bin/env python3
"""
Offline version of Gas Station Finder for testing without internet
"""

import math
from typing import List, Dict

class GasStationFinderOffline:
    def __init__(self):
        # User location (set manually for testing)
        self.user_lat = 40.7128  # New York City coordinates
        self.user_lon = -74.0060
        
        # Gas station data (mock data for prototype)
        self.gas_stations = self.load_mock_data()
    
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
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in miles using Haversine formula"""
        R = 3959  # Earth's radius in miles
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def search_gas_stations(self, sort_by: str = "closest", gas_type: str = "all", brand: str = "all"):
        """Search and display gas stations based on criteria"""
        print(f"📍 Your location: {self.user_lat:.6f}, {self.user_lon:.6f}")
        print(f"🔍 Searching with filters - Sort: {sort_by}, Gas Type: {gas_type}, Brand: {brand}")
        
        # Filter stations
        filtered_stations = []
        for station in self.gas_stations:
            # Apply brand filter
            if brand != "all" and station["brand"] != brand:
                continue
            
            # Calculate distance
            distance = self.calculate_distance(
                self.user_lat, self.user_lon,
                station["lat"], station["lon"]
            )
            
            station["distance"] = distance
            filtered_stations.append(station)
        
        # Sort based on criteria
        if sort_by == "closest":
            filtered_stations.sort(key=lambda x: x["distance"])
        elif sort_by == "cheapest":
            # Sort by cheapest gas type (E85, 87, 89, 91 in order of preference)
            def get_cheapest_price(station):
                prices = station["prices"]
                return min(prices.values())
            filtered_stations.sort(key=get_cheapest_price)
        elif sort_by == "gas_type":
            if gas_type != "all":
                filtered_stations.sort(key=lambda x: x["prices"].get(gas_type, float('inf')))
        elif sort_by == "brand":
            filtered_stations.sort(key=lambda x: x["brand"])
        
        # Display results
        print("\n" + "="*80)
        print("🏪 GAS STATION RESULTS")
        print("="*80)
        print(f"{'Station':<25} {'Brand':<10} {'Distance':<10} {'E85':<8} {'87':<8} {'89':<8} {'91':<8}")
        print("-"*80)
        
        for station in filtered_stations:
            prices = station["prices"]
            print(f"{station['name']:<25} {station['brand']:<10} {station['distance']:.2f} mi   "
                  f"${prices.get('E85', 'N/A'):<7} ${prices.get('87', 'N/A'):<7} "
                  f"${prices.get('89', 'N/A'):<7} ${prices.get('91', 'N/A'):<7}")
        
        print("="*80)
    
    def run_demo(self):
        """Run demonstration of all features"""
        print("🚗 Gas Station Finder - Demo Mode")
        print("="*50)
        print("📍 Using New York City as test location")
        print("🌐 This version works offline for testing")
        
        # Test different sorting options
        print("\n1. 🔍 Closest stations:")
        self.search_gas_stations("closest", "all", "all")
        
        print("\n2. 💰 Cheapest stations:")
        self.search_gas_stations("cheapest", "all", "all")
        
        print("\n3. ⛽ Filter by gas type (87 octane):")
        self.search_gas_stations("gas_type", "87", "all")
        
        print("\n4. 🏪 Filter by brand (Shell):")
        self.search_gas_stations("brand", "all", "Shell")
        
        print("\n5. 🎯 Combined filter (cheapest 87 octane from Shell):")
        self.search_gas_stations("cheapest", "87", "Shell")

def main():
    app = GasStationFinderOffline()
    app.run_demo()

if __name__ == "__main__":
    main()




