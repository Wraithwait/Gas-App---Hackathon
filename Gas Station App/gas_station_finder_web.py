#!/usr/bin/env python3
"""
Web-based Gas Station Finder using Flask
This version provides a web GUI that works without tkinter
"""

from flask import Flask, render_template, request, jsonify
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import json
import random
from typing import List, Dict
import math
import os
import sys
from dotenv import load_dotenv
from mapbox_integration import MapboxGasStationService

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Data Generation Logic (from Gas Stations.py) ---

BRAND_PREMIUMS = {
    "Shell": 0.35, "Arco": -0.10, "Chevron": 0.40, "Valero": 0.10,
    "Sinclair": 0.05, "76": 0.25, "Mobil": 0.20, "Circle K": 0.0,
    "Speedway Express": 0.0, "Chevron G & M": 0.40, "Chevron Extra Mile": 0.40,
    "Speedway": 0.0, "G & M Oil": 0.0, "AM/PM": -0.10, "Costco Gas Station": -0.20,
    "G & M Food Mart": 0.0, "Gas": 0.0, "AM / PM": -0.10
}

STATION_DEFINITIONS = [
    {"brand": "Shell", "street": "2249 Harbor Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6625, "lon": -117.9175},
    {"brand": "Arco", "street": "2490 Fairview Rd", "city": "Costa Mesa", "zip": "92626", "lat": 33.6844, "lon": -117.9085},
    {"brand": "Arco", "street": "2602 Newport Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6495, "lon": -117.9195},
    {"brand": "Arco", "street": "3201 Harbor Blvd", "city": "Costa Mesa", "zip": "92626", "lat": 33.6966, "lon": -117.9184},
    {"brand": "Arco", "street": "2021 Newport Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6416, "lon": -117.9130},
    {"brand": "Chevron", "street": "2160 Harbor Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6599, "lon": -117.9175},
    {"brand": "Chevron", "street": "3190 Harbor Blvd", "city": "Costa Mesa", "zip": "92626", "lat": 33.6959, "lon": -117.9184},
    {"brand": "Valero", "street": "2050 Harbor Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6570, "lon": -117.9176},
    {"brand": "Arco", "street": "3003 Newport Blvd", "city": "Costa Mesa", "zip": "92626", "lat": 33.6616, "lon": -117.9273},
    {"brand": "Shell", "street": "1201 Baker St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6888, "lon": -117.8926},
    {"brand": "Sinclair", "street": "2502 Harbor Blvd", "city": "Costa Mesa", "zip": "92626", "lat": 33.6766, "lon": -117.9179},
    {"brand": "Arco", "street": "300 Bristol St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6917, "lon": -117.8805},
    {"brand": "76", "street": "1195 Baker St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6886, "lon": -117.8920},
    {"brand": "Mobil", "street": "3006 Harbor Blvd", "city": "Costa Mesa", "zip": "92626", "lat": 33.6896, "lon": -117.9183},
    {"brand": "Circle K", "street": "3006 Harbor Blvd", "city": "Costa Mesa", "zip": "92626", "lat": 33.6896, "lon": -117.9183},
    {"brand": "Chevron", "street": "3000 Fairview Rd", "city": "Costa Mesa", "zip": "92626", "lat": 33.6946, "lon": -117.9084},
    {"brand": "Chevron", "street": "1740 Newport Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6366, "lon": -117.9090},
    {"brand": "Gas", "street": "2281 Newport Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6457, "lon": -117.9158},
    {"brand": "Shell", "street": "1512 Bristol St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6784, "lon": -117.8888},
    {"brand": "76", "street": "1900 Newport Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6393, "lon": -117.9116},
    {"brand": "Speedway Express", "street": "799 W 19th St", "city": "Costa Mesa", "zip": "92627", "lat": 33.6517, "lon": -117.9290},
    {"brand": "Chevron G & M", "street": "3048 Bristol St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6931, "lon": -117.8829},
    {"brand": "Chevron", "street": "2995 Bristol St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6932, "lon": -117.8814},
    {"brand": "Chevron Extra Mile - G & M", "street": "1740 Newport Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6366, "lon": -117.9090},
    {"brand": "Chevron Extra Mile", "street": "195 E 17th St", "city": "Costa Mesa", "zip": "92627", "lat": 33.6415, "lon": -117.9077},
    {"brand": "Mobil", "street": "3470 Fairview Rd", "city": "Costa Mesa", "zip": "92626", "lat": 33.7042, "lon": -117.9086},
    {"brand": "Speedway", "street": "751 Baker St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6874, "lon": -117.8860},
    {"brand": "Arco", "street": "2100 SE Bristol St", "city": "Newport Beach", "zip": "92660", "lat": 33.6706, "lon": -117.8719},
    {"brand": "G & M Oil", "street": "3067 Bristol St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6945, "lon": -117.8839},
    {"brand": "76", "street": "393 E 17th St", "city": "Costa Mesa", "zip": "92627", "lat": 33.6433, "lon": -117.9050},
    {"brand": "AM/PM", "street": "2602 Newport Blvd", "city": "Costa Mesa", "zip": "92627", "lat": 33.6495, "lon": -117.9195},
    {"brand": "Arco", "street": "3414 S Main St", "city": "Santa Ana", "zip": "92707", "lat": 33.7011, "lon": -117.8717},
    {"brand": "Costco Gas Station", "street": "17900 Newhope St", "city": "Fountain Valley", "zip": "92708", "lat": 33.7145, "lon": -117.9351},
    {"brand": "Chevron", "street": "2121 SE Bristol St", "city": "Newport Beach", "zip": "92660", "lat": 33.6713, "lon": -117.8726},
    {"brand": "Shell", "street": "3820 S Fairview St", "city": "Santa Ana", "zip": "92704", "lat": 33.7032, "lon": -117.8961},
    {"brand": "Chevron", "street": "3801 S Bristol St", "city": "Santa Ana", "zip": "92704", "lat": 33.7045, "lon": -117.8806},
    {"brand": "Chevron", "street": "1550 Jamboree Rd", "city": "Newport Beach", "zip": "92660", "lat": 33.6414, "lon": -117.8687},
    {"brand": "G & M Food Mart", "street": "790 W 19th St", "city": "Costa Mesa", "zip": "92627", "lat": 33.6511, "lon": -117.9287},
    {"brand": "Chevron", "street": "3301 S Bristol St", "city": "Santa Ana", "zip": "92704", "lat": 33.7088, "lon": -117.8814},
    {"brand": "Chevron", "street": "301 East Coast Hwy", "city": "Newport Beach", "zip": "92660", "lat": 33.6120, "lon": -117.8986},
    {"brand": "AM / PM", "street": "300 Bristol St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6917, "lon": -117.8805},
    {"brand": "G & M Food Mart", "street": "3067 Bristol St", "city": "Costa Mesa", "zip": "92626", "lat": 33.6945, "lon": -117.8839},
    {"brand": "AM / PM", "street": "3003 Newport Blvd", "city": "Costa Mesa", "zip": "92626", "lat": 33.6616, "lon": -117.9273},
]

def generate_station_data():
    stations_output = {}
    area_base_price = random.uniform(4.80, 5.10)
    for i, station_def in enumerate(STATION_DEFINITIONS):
        station_id = f"OC-{i+1:02d}"
        brand = station_def['brand']
        premium = BRAND_PREMIUMS.get(brand, 0.0)
        station_randomness = random.uniform(-0.05, 0.05)
        price_reg = round(area_base_price + premium + station_randomness, 2)
        price_mid = round(price_reg + 0.20, 2)
        price_prem = round(price_reg + 0.40, 2)
        station_data = {
            "station_id": station_id, "brand_name": brand,
            "address": {"street": station_def['street'], "zip_code": station_def['zip']},
            "location": {"latitude": station_def['lat'], "longitude": station_def['lon']},
            "prices": {
                "regular": price_reg, "midgrade": price_mid, "premium": price_prem,
                "diesel": round(price_reg + 0.60, 2) if random.random() < 0.7 else None,
                "e85": round(price_reg - 0.50, 2) if random.random() < 0.25 else None
            }
        }
        stations_output[station_id] = station_data
    return stations_output

def save_as_json(stations_dict, filename):
    with open(filename, 'w') as f:
        json.dump(stations_dict, f, indent=2)

# --- End of Data Generation Logic ---

class GasStationFinderWeb:
    def __init__(self):
        # Initialize Mapbox API service
        self.mapbox_access_token = os.getenv('MAPBOX_ACCESS_TOKEN')
        if self.mapbox_access_token:
            self.mapbox_service = MapboxGasStationService(self.mapbox_access_token)
            self.use_real_data = True
        else:
            self.mapbox_service = None
            self.use_real_data = False
            print("⚠️  MAPBOX_ACCESS_TOKEN not set. Using mock data.")
        
        # Load station data from JSON file, which is the primary source of truth
        self.gas_stations = self.load_stations_from_json('stations.json')
        if not self.gas_stations:
            print("⚠️ Could not load station data from stations.json. The app may not function correctly.")
        
        # Dynamically get a unique list of brands from the loaded stations
        self.available_brands = sorted(list(set(s['brand'] for s in self.gas_stations if s.get('brand'))))
    
    def load_stations_from_json(self, filepath: str) -> List[Dict]:
        """Load gas station data from a JSON file."""
        # ========================================
        # HOOK: GAS PRICING INFORMATION SOURCE
        # ========================================
        # This is where gas station data is loaded from a static file.
        # To update the data, run 'Gas Stations.py' manually.
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            stations_list = []
            for station_id, station_data in data.items():
                # Map fuel types from JSON to application's expected keys
                prices = station_data.get("prices", {})
                mapped_prices = {
                    "E85": prices.get("e85"),
                    "87": prices.get("regular"),
                    "89": prices.get("midgrade"),
                    "91": prices.get("premium"),
                    "diesel": prices.get("diesel")
                }

                # Construct full address string
                addr = station_data.get("address", {})
                full_address = f"{addr.get('street', '')}, {addr.get('zip_code', '')}"

                stations_list.append({
                    "name": station_data.get('brand_name', 'Unknown Station'),
                    "brand": station_data.get("brand_name"),
                    "lat": station_data.get("location", {}).get("latitude"),
                    "lon": station_data.get("location", {}).get("longitude"),
                    "address": full_address,
                    "prices": {k: v for k, v in mapped_prices.items() if v is not None}
                })
            return stations_list
        except FileNotFoundError:
            print(f"❌ CRITICAL ERROR: The data file '{filepath}' was not found.")
            print("💡 Please create a 'stations.json' file or run 'Gas Stations.py' to generate it.")
            return []
        except json.JSONDecodeError:
            print(f"❌ CRITICAL ERROR: Could not decode JSON from '{filepath}'. The file might be corrupt.")
            return []
        except Exception as e:
            print(f"❌ An unexpected error occurred while loading '{filepath}': {e}")
            return []
    
    def get_user_location(self, address: str) -> tuple:
        """Get user's coordinates from address input"""
        try:
            geolocator = Nominatim(user_agent="gas_station_finder")
            location = geolocator.geocode(address)
            
            if location:
                return location.latitude, location.longitude, location.address
            else:
                return None, None, "Address not found"
                
        except Exception as e:
            return None, None, f"Error: {str(e)}"
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in miles"""
        return geodesic((lat1, lon1), (lat2, lon2)).miles
    
    def search_gas_stations(self, user_lat: float, user_lon: float, sort_by: str = "closest", 
                          gas_type: str = "all", brand: str = "all") -> List[Dict]:
        """Search and return gas stations based on criteria"""
        # ========================================
        # HOOK: GAS STATION SEARCH AND FILTERING
        # ========================================
        # This method processes the search criteria and filters gas stations
        # Input: user coordinates, sort preferences, gas type filter, brand filter
        # Output: List of filtered and sorted gas stations with pricing data
        # Integration point: Add real-time price updates, availability checks

        # Create a fresh copy of stations to process for this search
        stations_to_process = [s.copy() for s in self.gas_stations]

        # Always use straight-line ("as the crow flies") distance
        for station in stations_to_process:
            # Calculate distance
            distance = self.calculate_distance(
                user_lat, user_lon, station["lat"], station["lon"])
            station["distance"] = round(distance, 2)
            
            # Estimate travel time assuming an average speed of 30 mph
            # (distance / speed) * 60 minutes/hour
            if distance < float('inf'):
                estimated_time_minutes = (distance / 30) * 60
                station['duration'] = round(estimated_time_minutes)
        
        # 2. Filter the processed stations list in-place
        results = []
        for station in stations_to_process: # Use the list that has distance/duration data

            # Apply brand filter
            if brand != "all" and station.get("brand", "").lower() != brand.lower():
                continue
            # Apply gas type filter
            if gas_type != "all" and gas_type not in station.get("prices", {}):
                continue
            results.append(station)

        return results

# Initialize the finder
finder = GasStationFinderWeb()

@app.route('/')
def index():
    # Pass the list of available brands to the template
    return render_template('index.html', 
                           mapbox_token=finder.mapbox_access_token, 
                           brands=finder.available_brands)

@app.route('/geocode', methods=['POST'])
def geocode():
    # ========================================
    # HOOK: LOCATION SEARCH FIELD PROCESSING
    # ========================================
    # This endpoint handles the address input from the search field
    # Input: JSON with 'address' field from the frontend
    # Output: Latitude/longitude coordinates for the entered address
    # Integration point: Connect to real geocoding services here
    
    data = request.get_json()
    address = data.get('address', '')
    
    lat, lon, message = finder.get_user_location(address)
    
    if lat and lon:
        return jsonify({
            'success': True,
            'lat': lat,
            'lon': lon,
            'address': message
        })
    else:
        return jsonify({
            'success': False,
            'message': message
        })

@app.route('/search', methods=['POST'])
def search():
    # ========================================
    # HOOK: SEARCH FILTERS AND SORTING
    # ========================================
    # This endpoint processes all search criteria from the frontend
    # Input fields processed:
    # - sort_by: 'closest', 'cheapest', 'gas_type', 'brand'
    # - gas_type: 'all', 'E85', '87', '89', '91'
    # - brand: 'all', 'Shell', 'Exxon', 'BP', 'Chevron', 'Mobil', 'Speedway', '7-Eleven'
    # Integration point: Connect to real gas station APIs here
    
    data = request.get_json()
    
    user_lat = data.get('lat')
    user_lon = data.get('lon')
    sort_by = data.get('sort_by', 'closest')
    gas_type = data.get('gas_type', 'all')
    brand = data.get('brand', 'all')
    
    if not user_lat or not user_lon:
        return jsonify({'error': 'Location not set'})
    
    results = finder.search_gas_stations(user_lat, user_lon, sort_by, gas_type, brand)
    
    return jsonify({
        'success': True,
        'results': results
    })

@app.route('/all-stations', methods=['GET'])
def all_stations():
    """Returns the complete list of all gas stations from the data source."""
    # The 'distance' key will be missing, which the frontend will handle.
    return jsonify({
        'success': True,
        'results': finder.gas_stations
    })

@app.route('/refresh-data', methods=['POST'])
def refresh_data():
    """Generates a new stations.json file with updated prices."""
    try:
        print("🔄 Regenerating station data file...")
        station_data_dict = generate_station_data()
        save_as_json(station_data_dict, 'stations.json')
        return jsonify({'success': True, 'message': 'Station data has been refreshed.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/travel-info', methods=['POST'])
def get_travel_info():
    """Get travel time and directions to a gas station"""
    # ========================================
    # HOOK: TRAVEL INFORMATION API
    # ========================================
    # This endpoint provides travel time and directions
    # Input: origin coordinates, destination coordinates, travel mode
    # Output: Travel time, distance, and route information
    # Integration point: Connect to Google Directions API or other routing services
    
    data = request.get_json()
    
    origin_lat = data.get('origin_lat')
    origin_lon = data.get('origin_lon')
    dest_lat = data.get('dest_lat')
    dest_lon = data.get('dest_lon')
    mode = data.get('mode', 'driving')
    
    if not all([origin_lat, origin_lon, dest_lat, dest_lon]):
        return jsonify({'error': 'Missing coordinates'})
    
    # Use Mapbox API if available
    if finder.use_real_data and finder.mapbox_service:
        try:
            origin = (float(origin_lat), float(origin_lon))
            destination = (float(dest_lat), float(dest_lon))
            
            # Map mode names to Mapbox profiles
            profile_map = {
                'driving': 'driving',
                'walking': 'walking',
                'bicycling': 'cycling',
                'transit': 'driving'  # Mapbox doesn't have transit in basic plan
            }
            mapbox_profile = profile_map.get(mode, 'driving')
            
            travel_info = finder.mapbox_service.get_directions(origin, destination, mapbox_profile)
            
            if travel_info:
                return jsonify({
                    'success': True,
                    'travel_info': travel_info
                })
            else:
                return jsonify({'error': 'Could not get travel information'})
                
        except Exception as e:
            return jsonify({'error': f'Error getting travel info: {str(e)}'})
    else:
        # Fallback: Calculate straight-line distance
        distance = finder.calculate_distance(
            float(origin_lat), float(origin_lon),
            float(dest_lat), float(dest_lon)
        )
        
        # Estimate travel time (assuming 30 mph average)
        estimated_time_minutes = (distance / 30) * 60
        
        return jsonify({
            'success': True,
            'travel_info': {
                'distance_text': f"{distance:.1f} miles",
                'distance_meters': distance * 1609.34,
                'duration_text': f"{int(estimated_time_minutes)} min",
                'duration_seconds': int(estimated_time_minutes * 60),
                'start_address': 'Origin',
                'end_address': 'Destination',
                'note': 'Estimated travel time (straight-line distance)'
            }
        })

@app.route('/station-details', methods=['POST'])
def get_station_details():
    """Get detailed information about a specific gas station"""
    # ========================================
    # HOOK: STATION DETAILS API
    # ========================================
    # This endpoint provides detailed information about a specific station
    # Input: place_id or station coordinates
    # Output: Detailed station information, photos, reviews, etc.
    
    data = request.get_json()
    place_id = data.get('place_id')
    
    if not place_id:
        return jsonify({'error': 'Place ID required'})
    
    if finder.use_real_data and finder.mapbox_service:
        try:
            # Mapbox doesn't have detailed place information like Google Places
            # We can use the place_id to get basic info from our search results
            # For now, return a basic response
            return jsonify({
                'success': True,
                'details': {
                    'name': 'Gas Station',
                    'formatted_address': 'Address not available',
                    'rating': 'N/A',
                    'user_ratings_total': 0,
                    'formatted_phone_number': 'Not available',
                    'website': None,
                    'business_status': 'OPERATIONAL',
                    'photos': []
                }
            })
                
        except Exception as e:
            return jsonify({'error': f'Error getting station details: {str(e)}'})
    else:
        return jsonify({'error': 'Mapbox API not available'})

if __name__ == '__main__':
    import socket
    
    def is_port_available(port):
        """Check if a port is available"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return True
            except OSError:
                return False
    
    print("🌐 Starting Gas Station Finder Web Interface...")
    
    # Try different ports if 5000 is in use
    ports_to_try = [5000, 5001, 5002, 8000, 8080]
    selected_port = None
    
    for port in ports_to_try:
        if is_port_available(port):
            selected_port = port
            break
        else:
            print(f"❌ Port {port} is already in use, trying next port...")
    
    if selected_port is None:
        print("❌ Could not find an available port.")
        print("💡 Try running: pkill -f 'python3 gas_station_finder_web.py'")
        print("💡 Or use: python3 start_app.py stop")
        sys.exit(1)
    
    print(f"📱 Starting server on port {selected_port}...")
    print(f"🌐 Open your browser and go to: http://localhost:{selected_port}")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=selected_port, use_reloader=False)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
