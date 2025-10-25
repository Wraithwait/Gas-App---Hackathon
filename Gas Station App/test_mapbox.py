#!/usr/bin/env python3
"""
Test script for Mapbox integration
"""

import os
from mapbox_integration import MapboxGasStationService

def test_mapbox_integration():
    print("🧪 Testing Mapbox Integration...")
    
    # Get access token from environment
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')
    
    if not access_token:
        print("❌ MAPBOX_ACCESS_TOKEN not set")
        print("Please set your Mapbox access token:")
        print("export MAPBOX_ACCESS_TOKEN='your_token_here'")
        return False
    
    try:
        # Initialize service
        service = MapboxGasStationService(access_token)
        print("✅ Mapbox service initialized")
        
        # Test geocoding
        print("\n📍 Testing geocoding...")
        coords = service.geocode_address("Times Square, New York")
        if coords:
            print(f"✅ Geocoding successful: {coords}")
            lat, lon = coords
        else:
            print("❌ Geocoding failed")
            return False
        
        # Test POI search
        print("\n🔍 Testing POI search...")
        stations = service.search_poi(lat, lon, radius=2000, poi_type='gas_station')
        print(f"✅ Found {len(stations)} gas stations")
        
        if stations:
            # Show first few stations
            for i, station in enumerate(stations[:3]):
                print(f"  {i+1}. {station['name']} - {station['distance']:.2f} mi")
        
        # Test directions
        if stations:
            print("\n🚗 Testing directions...")
            origin = (lat, lon)
            destination = (stations[0]['lat'], stations[0]['lon'])
            
            directions = service.get_directions(origin, destination)
            if directions:
                print(f"✅ Directions successful:")
                print(f"  Duration: {directions['duration_text']}")
                print(f"  Distance: {directions['distance_text']}")
            else:
                print("❌ Directions failed")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_mapbox_integration()
