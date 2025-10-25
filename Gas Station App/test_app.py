#!/usr/bin/env python3
"""
Test script to verify the gas station finder functionality
"""

from gas_station_finder_cli import GasStationFinderCLI

def test_app():
    print("🧪 Testing Gas Station Finder...")
    
    # Create app instance
    app = GasStationFinderCLI()
    
    # Test location setting
    print("\n1. Testing location setting...")
    success = app.get_user_location("123 Main St, New York, NY")
    if success:
        print("✅ Location setting works!")
    else:
        print("❌ Location setting failed!")
        return
    
    # Test gas station search
    print("\n2. Testing gas station search...")
    app.search_gas_stations("closest", "all", "all")
    
    print("\n3. Testing with different filters...")
    app.search_gas_stations("cheapest", "87", "Shell")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_app()




