#!/usr/bin/env python3
"""
Debug script to test Mapbox API responses
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def debug_mapbox_search():
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')
    
    if not access_token:
        print("❌ MAPBOX_ACCESS_TOKEN not set")
        return
    
    print("🔍 Debugging Mapbox API...")
    
    # Test different search queries
    queries = [
        "gas station",
        "fuel station", 
        "shell",
        "exxon",
        "gas"
    ]
    
    lat, lon = 40.75665, -73.986851  # Times Square
    
    for query in queries:
        print(f"\n🔍 Testing query: '{query}'")
        
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json"
        params = {
            'proximity': f"{lon},{lat}",
            'types': 'poi',
            'limit': 5,
            'access_token': access_token
        }
        
        try:
            response = requests.get(url, params=params)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                features = data.get('features', [])
                print(f"Found {len(features)} results")
                
                for i, feature in enumerate(features[:3]):
                    props = feature.get('properties', {})
                    name = props.get('name', 'Unknown')
                    category = props.get('category', 'Unknown')
                    print(f"  {i+1}. {name} - {category}")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    debug_mapbox_search()

