#!/usr/bin/env python3
"""
Command-line version of Gas Station Finder
This version doesn't require tkinter and can be run immediately
"""

import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import json
from typing import List, Dict, Tuple
import math

class GasStationFinderCLI:
    def __init__(self):
        # User location
        self.user_lat = None
        self.user_lon = None
        
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
    
    def get_user_location(self, address: str) -> bool:
        """Get user's coordinates from address input"""
        if not address.strip():
            print("❌ Please enter an address")
            return False
        
        try:
            geolocator = Nominatim(user_agent="gas_station_finder")
            location = geolocator.geocode(address)
            
            if location:
                self.user_lat = location.latitude
                self.user_lon = location.longitude
                print(f"✅ Location found: {location.address}")
                print(f"📍 Coordinates: {self.user_lat:.6f}, {self.user_lon:.6f}")
                return True
            else:
                print("❌ Address not found. Please try a different address.")
                return False
                
        except Exception as e:
            print(f"❌ Error getting location: {str(e)}")
            return False
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in miles"""
        return geodesic((lat1, lon1), (lat2, lon2)).miles
    
    def search_gas_stations(self, sort_by: str = "closest", gas_type: str = "all", brand: str = "all"):
        """Search and display gas stations based on criteria"""
        if not self.user_lat or not self.user_lon:
            print("❌ Please get your location first!")
            return
        
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
    
    def run(self):
        """Main application loop"""
        print("🚗 Welcome to Gas Station Finder!")
        print("="*50)
        
        while True:
            print("\n📋 MENU:")
            print("1. Set your location")
            print("2. Find gas stations")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                address = input("Enter your address: ").strip()
                self.get_user_location(address)
            
            elif choice == "2":
                if not self.user_lat or not self.user_lon:
                    print("❌ Please set your location first!")
                    continue
                
                print("\n🔍 Search Options:")
                print("Sort by: closest, cheapest, gas_type, brand")
                sort_by = input("Sort by (default: closest): ").strip() or "closest"
                
                print("Gas types: all, E85, 87, 89, 91")
                gas_type = input("Filter by gas type (default: all): ").strip() or "all"
                
                print("Brands: all, Shell, Exxon, BP, Chevron, Mobil, Speedway, 7-Eleven")
                brand = input("Filter by brand (default: all): ").strip() or "all"
                
                self.search_gas_stations(sort_by, gas_type, brand)
            
            elif choice == "3":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")

def main():
    app = GasStationFinderCLI()
    app.run()

if __name__ == "__main__":
    main()




