#!/usr/bin/env python3
"""
Google Places API Integration for Gas Station Finder
Provides real-time gas station data and travel information
"""

import requests
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import os

class GooglePlacesGasStationService:
    def __init__(self, api_key: str):
        self.api_key = AIzaSyAlrN3ixVR2QbQMLF5QkIsjtJefsK1tyQ8
        self.base_url = "https://maps.googleapis.com/maps/api"
        self.session = requests.Session()
    
    def search_gas_stations(self, lat: float, lon: float, radius: int = 5000) -> List[Dict]:
        """
        Search for gas stations near a location using Google Places API
        
        Args:
            lat: Latitude of search center
            lon: Longitude of search center  
            radius: Search radius in meters (max 50000)
        
        Returns:
            List of gas station data
        """
        url = f"{self.base_url}/place/nearbysearch/json"
        
        params = {
            'location': f"{lat},{lon}",
            'radius': min(radius, 50000),  # Google's max radius
            'type': 'gas_station',
            'key': self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') != 'OK':
                raise Exception(f"Google Places API error: {data.get('status')}")
            
            gas_stations = []
            for place in data.get('results', []):
                station_data = self._process_place_data(place)
                if station_data:
                    gas_stations.append(station_data)
            
            return gas_stations
            
        except requests.RequestException as e:
            print(f"Error fetching gas stations: {e}")
            return []
    
    def _process_place_data(self, place: Dict) -> Optional[Dict]:
        """Process raw Google Places data into our format"""
        try:
            # Extract basic information
            name = place.get('name', 'Unknown Station')
            place_id = place.get('place_id')
            rating = place.get('rating', 0)
            user_ratings_total = place.get('user_ratings_total', 0)
            
            # Extract location
            location = place.get('geometry', {}).get('location', {})
            lat = location.get('lat')
            lon = location.get('lng')
            
            if not lat or not lon:
                return None
            
            # Extract address
            address = place.get('vicinity', 'Address not available')
            
            # Extract business status
            business_status = place.get('business_status', 'UNKNOWN')
            
            # Extract opening hours
            opening_hours = place.get('opening_hours', {})
            is_open_now = opening_hours.get('open_now', None)
            
            # Extract price level (if available)
            price_level = place.get('price_level', None)
            
            # Extract photos (if available)
            photos = place.get('photos', [])
            photo_reference = photos[0].get('photo_reference') if photos else None
            
            return {
                'name': name,
                'place_id': place_id,
                'brand': self._extract_brand(name),
                'lat': lat,
                'lon': lon,
                'address': address,
                'rating': rating,
                'user_ratings_total': user_ratings_total,
                'business_status': business_status,
                'is_open_now': is_open_now,
                'price_level': price_level,
                'photo_reference': photo_reference,
                'prices': self._get_fuel_prices(place_id),  # This would need separate API calls
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error processing place data: {e}")
            return None
    
    def _extract_brand(self, name: str) -> str:
        """Extract brand from station name"""
        name_lower = name.lower()
        brands = ['shell', 'exxon', 'bp', 'chevron', 'mobil', 'speedway', '7-eleven', 
                 'valero', 'phillips 66', 'citgo', 'marathon', 'sunoco', 'texaco']
        
        for brand in brands:
            if brand in name_lower:
                return brand.title()
        
        return 'Other'
    
    def _get_fuel_prices(self, place_id: str) -> Dict[str, float]:
        """
        Get fuel prices for a specific gas station
        Note: Google Places API doesn't provide fuel prices directly
        This would need integration with fuel price APIs like GasBuddy
        """
        # For now, return mock prices - in production, integrate with fuel price APIs
        return {
            'E85': 2.89,
            '87': 3.45,
            '89': 3.65,
            '91': 3.85
        }
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed information about a specific place"""
        url = f"{self.base_url}/place/details/json"
        
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,geometry,rating,user_ratings_total,opening_hours,photos,price_level,website,formatted_phone_number',
            'key': self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                return data.get('result')
            else:
                print(f"Error getting place details: {data.get('status')}")
                return None
                
        except requests.RequestException as e:
            print(f"Error fetching place details: {e}")
            return None
    
    def get_travel_time(self, origin: Tuple[float, float], destination: Tuple[float, float], 
                       mode: str = 'driving') -> Optional[Dict]:
        """
        Get travel time and distance between two points
        
        Args:
            origin: (lat, lon) of starting point
            destination: (lat, lon) of destination
            mode: 'driving', 'walking', 'bicycling', 'transit'
        
        Returns:
            Dict with travel time, distance, and route information
        """
        url = f"{self.base_url}/directions/json"
        
        params = {
            'origin': f"{origin[0]},{origin[1]}",
            'destination': f"{destination[0]},{destination[1]}",
            'mode': mode,
            'key': self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                route = data.get('routes', [{}])[0]
                leg = route.get('legs', [{}])[0]
                
                return {
                    'duration_text': leg.get('duration', {}).get('text'),
                    'duration_seconds': leg.get('duration', {}).get('value'),
                    'distance_text': leg.get('distance', {}).get('text'),
                    'distance_meters': leg.get('distance', {}).get('value'),
                    'start_address': leg.get('start_address'),
                    'end_address': leg.get('end_address'),
                    'steps': leg.get('steps', []),
                    'overview_polyline': route.get('overview_polyline', {}).get('points')
                }
            else:
                print(f"Error getting directions: {data.get('status')}")
                return None
                
        except requests.RequestException as e:
            print(f"Error fetching directions: {e}")
            return None
    
    def get_photo_url(self, photo_reference: str, max_width: int = 400) -> str:
        """Get photo URL for a place"""
        return f"{self.base_url}/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={self.api_key}"
    
    def search_with_filters(self, lat: float, lon: float, radius: int = 5000,
                           min_rating: float = 0, open_now: bool = False) -> List[Dict]:
        """
        Search for gas stations with additional filters
        
        Args:
            lat: Latitude of search center
            lon: Longitude of search center
            radius: Search radius in meters
            min_rating: Minimum rating filter
            open_now: Only return stations open now
        
        Returns:
            List of filtered gas stations
        """
        stations = self.search_gas_stations(lat, lon, radius)
        
        # Apply filters
        filtered_stations = []
        for station in stations:
            # Rating filter
            if station.get('rating', 0) < min_rating:
                continue
            
            # Open now filter
            if open_now and station.get('is_open_now') is False:
                continue
            
            filtered_stations.append(station)
        
        return filtered_stations

# Example usage and testing
def main():
    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        print("Please set GOOGLE_PLACES_API_KEY environment variable")
        return
    
    # Initialize service
    service = GooglePlacesGasStationService(api_key)
    
    # Example: Search for gas stations near Times Square
    times_square_lat = 40.7589
    times_square_lon = -73.9851
    
    print("🔍 Searching for gas stations near Times Square...")
    stations = service.search_gas_stations(times_square_lat, times_square_lon, radius=2000)
    
    print(f"Found {len(stations)} gas stations:")
    for station in stations[:5]:  # Show first 5
        print(f"📍 {station['name']} - {station['address']}")
        print(f"   Rating: {station['rating']}/5 ({station['user_ratings_total']} reviews)")
        print(f"   Open Now: {station['is_open_now']}")
        print(f"   Distance: {station.get('distance', 'N/A')} miles")
        print()
    
    # Example: Get travel time to first station
    if stations:
        first_station = stations[0]
        origin = (times_square_lat, times_square_lon)
        destination = (first_station['lat'], first_station['lon'])
        
        print(f"🚗 Travel time to {first_station['name']}:")
        travel_info = service.get_travel_time(origin, destination)
        if travel_info:
            print(f"   Duration: {travel_info['duration_text']}")
            print(f"   Distance: {travel_info['distance_text']}")

if __name__ == "__main__":
    main()

