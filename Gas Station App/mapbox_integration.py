#!/usr/bin/env python3
"""
Mapbox API Integration for Gas Station Finder
Provides real-time gas station data and travel information using Mapbox APIs
"""

import requests
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import os

class MapboxGasStationService:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.mapbox.com"
        self.session = requests.Session()
    
    def search_poi(self, lat: float, lon: float, radius: int = 5000, 
               poi_type: str = "gas_station") -> List[Dict]:
        """
        Search for Points of Interest using Mapbox Geocoding API
        
        Args:
            lat: Latitude of search center
            lon: Longitude of search center  
            radius: Search radius in meters
            poi_type: Type of POI to search for
        
        Returns:
            List of POI data
        """
        # Try multiple search strategies
        search_queries = [
            "gas station",
            "fuel station", 
            "gas",
            "shell",
            "exxon",
            "bp",
            "chevron"
        ]
        
        all_stations = []
        
        for query in search_queries:
            try:
                url = f"{self.base_url}/geocoding/v5/mapbox.places/{query}.json"
                
                params = {
                    'proximity': f"{lon},{lat}",
                    'types': 'poi',
                    'limit': 10,
                    'access_token': self.access_token
                }
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                for feature in data.get('features', []):
                    station_data = self._process_poi_data(feature, lat, lon)
                    if station_data and self._is_gas_station(station_data):
                        # Avoid duplicates
                        if not any(s['name'] == station_data['name'] for s in all_stations):
                            all_stations.append(station_data)
                
            except requests.RequestException as e:
                print(f"Error fetching POI data for '{query}': {e}")
                continue
        
        return all_stations
    
    def _process_poi_data(self, feature: Dict, user_lat: float, user_lon: float) -> Optional[Dict]:
        """Process Mapbox POI data into our format"""
        try:
            # Extract basic information
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            coordinates = geometry.get('coordinates', [])
            
            if len(coordinates) < 2:
                return None
            
            lon, lat = coordinates[0], coordinates[1]
            
            # Extract name and address
            name = properties.get('name', 'Unknown Station')
            address = properties.get('address', 'Address not available')
            
            # Extract category information
            category = properties.get('category', '')
            brand = self._extract_brand_from_category(category, name)
            
            # Calculate distance
            distance = self._calculate_distance(user_lat, user_lon, lat, lon)
            
            return {
                'name': name,
                'brand': brand,
                'lat': lat,
                'lon': lon,
                'address': address,
                'category': category,
                'distance': round(distance, 2),
                'place_id': feature.get('id', ''),
                'prices': self._get_fuel_prices(),  # Mock prices - would need fuel price API
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error processing POI data: {e}")
            return None
    
    def _is_gas_station(self, station_data: Dict) -> bool:
        """Check if a POI is actually a gas station"""
        name = station_data.get('name', '').lower()
        category = station_data.get('category', '').lower()
        
        # Keywords that indicate gas stations
        gas_keywords = ['gas', 'fuel', 'petrol', 'station', 'shell', 'exxon', 'bp', 
                       'chevron', 'mobil', 'speedway', 'valero', 'citgo', 'marathon',
                       'sunoco', 'texaco', 'arco', '7-eleven', 'conoco', 'phillips']
        
        # Check if any gas keywords are in the name or category
        for keyword in gas_keywords:
            if keyword in name or keyword in category:
                return True
        
        return False
    
    def _extract_brand_from_category(self, category: str, name: str) -> str:
        """Extract brand from category or name"""
        name_lower = name.lower()
        category_lower = category.lower()
        
        # Check name first
        brands = ['shell', 'exxon', 'bp', 'chevron', 'mobil', 'speedway', '7-eleven', 
                 'valero', 'phillips 66', 'citgo', 'marathon', 'sunoco', 'texaco',
                 'arco', 'costco', 'safeway', 'kroger']
        
        for brand in brands:
            if brand in name_lower:
                return brand.title()
        
        # Check category
        if 'gas' in category_lower or 'fuel' in category_lower:
            return 'Gas Station'
        
        return 'Other'
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in miles using Haversine formula"""
        import math
        
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
    
    def _get_fuel_prices(self) -> Dict[str, float]:
        """
        Get fuel prices for a gas station
        Note: Mapbox doesn't provide fuel prices directly
        This would need integration with fuel price APIs like GasBuddy
        """
        # For now, return mock prices - in production, integrate with fuel price APIs
        return {
            'E85': 2.89,
            '87': 3.45,
            '89': 3.65,
            '91': 3.85
        }
    
    def get_directions(self, origin: Tuple[float, float], destination: Tuple[float, float], 
                      profile: str = 'driving') -> Optional[Dict]:
        """
        Get directions between two points using Mapbox Directions API
        
        Args:
            origin: (lat, lon) of starting point
            destination: (lat, lon) of destination
            profile: 'driving', 'walking', 'cycling', 'driving-traffic'
        
        Returns:
            Dict with route information
        """
        # Mapbox expects lon,lat format
        origin_coords = f"{origin[1]},{origin[0]}"  # lon,lat
        dest_coords = f"{destination[1]},{destination[0]}"  # lon,lat

        url = f"{self.base_url}/directions/v5/mapbox/{profile}/{origin_coords};{dest_coords}"

        params = {
            'access_token': self.access_token,
            'geometries': 'geojson',
            'overview': 'full',
            'steps': 'true'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('routes'):
                route = data['routes'][0]
                leg = route['legs'][0]
                
                return {
                    'duration_text': f"{int(leg['duration'] / 60)} min",
                    'duration_seconds': leg['duration'],
                    'distance_text': f"{leg['distance'] / 1609.34:.1f} mi",
                    'distance_meters': leg['distance'],
                    'start_address': 'Origin',
                    'end_address': 'Destination',
                    'geometry': route.get('geometry'),
                    'steps': leg.get('steps', []),
                    'summary': route.get('summary', ''),
                    'profile': profile
                }
            else:
                print("No routes found")
                return None
                
        except requests.RequestException as e:
            print(f"Error getting directions: {e}")
            return None
    
    def get_matrix(self, coordinates: List[Tuple[float, float]], 
                   profile: str = 'driving') -> Optional[Dict]:
        """
        Get travel time matrix between multiple points
        
        Args:
            coordinates: List of (lat, lon) tuples
            profile: 'driving', 'walking', 'cycling'
        
        Returns:
            Matrix with travel times and distances
        """
        url = f"{self.base_url}/directions-matrix/v1/mapbox/{profile}"
        
        # Convert to lon,lat format
        coords_str = ";".join([f"{lon},{lat}" for lat, lon in coordinates])
        
        params = {
            'coordinates': coords_str,
            'access_token': self.access_token,
            'sources': '0',  # First coordinate is source
            'destinations': 'all'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                'durations': data.get('durations', []),
                'distances': data.get('distances', []),
                'sources': data.get('sources', []),
                'destinations': data.get('destinations', [])
            }
            
        except requests.RequestException as e:
            print(f"Error getting matrix: {e}")
            return None
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Geocode an address to coordinates
        
        Args:
            address: Address string to geocode
        
        Returns:
            (lat, lon) tuple or None
        """
        url = f"{self.base_url}/geocoding/v5/mapbox.places/{address}.json"
        
        params = {
            'access_token': self.access_token,
            'limit': 1
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('features'):
                feature = data['features'][0]
                coordinates = feature['geometry']['coordinates']
                return coordinates[1], coordinates[0]  # lat, lon
            else:
                return None
                
        except requests.RequestException as e:
            print(f"Error geocoding address: {e}")
            return None
    
    def search_with_filters(self, lat: float, lon: float, radius: int = 5000,
                           brand_filter: str = None) -> List[Dict]:
        """
        Search for gas stations with additional filters
        
        Args:
            lat: Latitude of search center
            lon: Longitude of search center
            radius: Search radius in meters
            brand_filter: Filter by specific brand
        
        Returns:
            List of filtered gas stations
        """
        stations = self.search_poi(lat, lon, radius, 'gas_station')
        
        # Apply brand filter
        if brand_filter and brand_filter.lower() != 'all':
            filtered_stations = []
            for station in stations:
                if brand_filter.lower() in station.get('brand', '').lower():
                    filtered_stations.append(station)
            return filtered_stations
        
        return stations

# Example usage and testing
def main():
    # Get access token from environment variable
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')
    
    if not access_token:
        print("Please set MAPBOX_ACCESS_TOKEN environment variable")
        return
    
    # Initialize service
    service = MapboxGasStationService(access_token)
    
    # Example: Search for gas stations near Times Square
    times_square_lat = 40.7589
    times_square_lon = -73.9851
    
    print("🔍 Searching for gas stations near Times Square...")
    stations = service.search_poi(times_square_lat, times_square_lon, radius=2000)
    
    print(f"Found {len(stations)} gas stations:")
    for station in stations[:5]:  # Show first 5
        print(f"📍 {station['name']} - {station['address']}")
        print(f"   Brand: {station['brand']}")
        print(f"   Distance: {station['distance']:.2f} miles")
        print()
    
    # Example: Get directions to first station
    if stations:
        first_station = stations[0]
        origin = (times_square_lat, times_square_lon)
        destination = (first_station['lat'], first_station['lon'])
        
        print(f"🚗 Travel time to {first_station['name']}:")
        directions = service.get_directions(origin, destination)
        if directions:
            print(f"   Duration: {directions['duration_text']}")
            print(f"   Distance: {directions['distance_text']}")

if __name__ == "__main__":
    main()
