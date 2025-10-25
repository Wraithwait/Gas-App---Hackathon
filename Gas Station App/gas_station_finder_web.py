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
from typing import List, Dict
import math
import os
import sys
from dotenv import load_dotenv
from mapbox_integration import MapboxGasStationService

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

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
        
        # Fallback to mock data if Mapbox API is not available
        self.gas_stations = self.load_mock_data()
    
    def load_mock_data(self) -> List[Dict]:
        """Load mock gas station data for prototype"""
        # ========================================
        # HOOK: GAS PRICING INFORMATION SOURCE
        # ========================================
        # This is where gas station data and pricing information is loaded
        # Current structure: name, brand, lat, lon, prices (E85, 87, 89, 91)
        # Integration point: Replace with real API calls to gas station databases
        # Data sources could include: GasBuddy API, AAA Fuel Finder, Google Places API
        
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
        
        # Use Mapbox API if available, otherwise fall back to mock data
        if self.use_real_data and self.mapbox_service:
            try:
                # Search for real gas stations using Mapbox API
                real_stations = self.mapbox_service.search_poi(user_lat, user_lon, radius=10000, poi_type='gas_station')
                
                # Distance is already calculated in Mapbox service
                # Use real data
                stations_to_filter = real_stations
            except Exception as e:
                print(f"Error fetching real gas stations: {e}")
                # Fall back to mock data
                stations_to_filter = self.gas_stations
        else:
            # Use mock data
            stations_to_filter = self.gas_stations
        
        # Filter stations
        filtered_stations = []
        for station in stations_to_filter:
            # Apply brand filter
            if brand != "all" and station.get("brand", "").lower() != brand.lower():
                continue
            
            # Calculate distance if not already calculated
            if "distance" not in station:
                distance = self.calculate_distance(
                    user_lat, user_lon,
                    station["lat"], station["lon"]
                )
                station["distance"] = round(distance, 2)
            
            filtered_stations.append(station)
        
        # Sort based on criteria
        if sort_by == "closest":
            filtered_stations.sort(key=lambda x: x["distance"])
        elif sort_by == "cheapest":
            def get_cheapest_price(station):
                prices = station.get("prices", {})
                if not prices:
                    return float('inf')
                return min(prices.values())
            filtered_stations.sort(key=get_cheapest_price)
        elif sort_by == "gas_type":
            if gas_type != "all":
                filtered_stations.sort(key=lambda x: x.get("prices", {}).get(gas_type, float('inf')))
        elif sort_by == "brand":
            filtered_stations.sort(key=lambda x: x.get("brand", ""))
        
        return filtered_stations

# Initialize the finder
finder = GasStationFinderWeb()

@app.route('/')
def index():
    return render_template('index.html')

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
