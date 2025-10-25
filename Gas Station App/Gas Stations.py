import json
import csv
import random

# --- Configuration ---
NUM_STATIONS_TO_GENERATE = 50
OUTPUT_JSON_FILE = 'stations.json'
OUTPUT_CSV_FILE = 'stations.csv'
# ---------------------

# Base data to create realistic fake stations
CITIES = [
    {"name": "Irvine", "zip": "92604", "lat": 33.68, "lon": -117.79},
    {"name": "Costa Mesa", "zip": "92627", "lat": 33.66, "lon": -117.91},
    {"name": "Newport Beach", "zip": "92663", "lat": 33.61, "lon": -117.93},
    {"name": "Anaheim", "zip": "92801", "lat": 33.84, "lon": -117.96},
    {"name": "Santa Ana", "zip": "92701", "lat": 33.76, "lon": -117.88},
    {"name": "Huntington Beach", "zip": "92648", "lat": 33.66, "lon": -117.99},
    {"name": "Fullerton", "zip": "92832", "lat": 33.86, "lon": -117.92},
    {"name": "Garden Grove", "zip": "92843", "lat": 33.78, "lon": -117.96},
    {"name": "Tustin", "zip": "92780", "lat": 33.74, "lon": -117.82},
    {"name": "Mission Viejo", "zip": "92691", "lat": 33.60, "lon": -117.66},
    {"name": "San Clemente", "zip": "92672", "lat": 33.43, "lon": -117.61},
    {"name": "Laguna Niguel", "zip": "92677", "lat": 33.52, "lon": -117.70},
    {"name": "Lake Forest", "zip": "92630", "lat": 33.65, "lon": -117.69},
]

BRANDS = [
    {"name": "Chevron", "premium": 0.40},
    {"name": "Shell", "premium": 0.35},
    {"name": "76", "premium": 0.25},
    {"name": "Mobil", "premium": 0.20},
    {"name": "ARCO", "premium": -0.10},
    {"name": "Costco", "premium": -0.20},
    {"name": "Sam's Club", "premium": -0.18},
    {"name": "OC Gas & Mart", "premium": 0.05},
    {"name": "Beach Stop Fuel", "premium": 0.10},
    {"name": "Speedy Gas", "premium": 0.0},
]

STREET_NAMES = [
    "Main St", "Culver Dr", "Harbor Blvd", "Beach Blvd", "Jamboree Rd",
    "MacArthur Blvd", "Euclid St", "Brookhurst St", "El Toro Rd",
    "Pacific Coast Hwy", "Barranca Pkwy", "Newport Blvd", "Edinger Ave"
]

def generate_stations(num_stations):
    """Generates a list of fake gas station data."""
    stations = []
    for i in range(num_stations):
        city = random.choice(CITIES)
        brand = random.choice(BRANDS)
        
        # --- Generate Prices ---
        base_price = round(random.uniform(4.90, 5.20) + brand["premium"], 3)
        prices = {
            "regular": base_price,
            "midgrade": round(base_price + 0.20, 3),
            "premium": round(base_price + 0.40, 3),
            # 70% chance of having diesel
            "diesel": round(base_price + 0.50, 3) if random.random() < 0.7 else None,
            # 25% chance of having E85
            "e85": round(base_price - 0.50, 3) if random.random() < 0.25 else None
        }
        
        # --- Generate Location ---
        # Add small random offset to lat/lon
        lat = city["lat"] + random.uniform(-0.05, 0.05)
        lon = city["lon"] + random.uniform(-0.05, 0.05)
        
        station = {
            "station_id": f"oc_{1001 + i}",
            "brand_name": brand["name"],
            "address": {
                "street": f"{random.randint(100, 9999)} {random.choice(STREET_NAMES)}",
                "city": city["name"],
                "state": "CA",
                "zip_code": city["zip"]
            },
            "location": {
                "latitude": round(lat, 5),
                "longitude": round(lon, 5)
            },
            "prices": prices,
            # Generate a fake timestamp from the "past" 24 hours
            "last_updated": f"2025-10-24T{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}Z"
        }
        stations.append(station)
        
    return stations

def save_as_json(stations, filename):
    """Saves the station list as a JSON file."""
    with open(filename, 'w') as f:
        json.dump(stations, f, indent=2)
    print(f"Successfully generated {filename}")

def save_as_csv(stations, filename):
    """Saves the station list as a CSV file."""
    if not stations:
        return
        
    # Flatten the data for CSV
    headers = [
        'station_id', 'brand_name', 'street_address', 'city', 'state', 'zip_code',
        'latitude', 'longitude', 'regular_price', 'midgrade_price', 
        'premium_price', 'diesel_price', 'e85_price', 'last_updated'
    ]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for station in stations:
            row = {
                'station_id': station['station_id'],
                'brand_name': station['brand_name'],
                'street_address': station['address']['street'],
                'city': station['address']['city'],
                'state': station['address']['state'],
                'zip_code': station['address']['zip_code'],
                'latitude': station['location']['latitude'],
                'longitude': station['location']['longitude'],
                'regular_price': station['prices']['regular'],
                'midgrade_price': station['prices']['midgrade'],
                'premium_price': station['prices']['premium'],
                'diesel_price': station['prices']['diesel'],
                'e85_price': station['prices']['e85'],
                'last_updated': station['last_updated']
            }
            writer.writerow(row)
            
    print(f"Successfully generated {filename}")

# --- Main execution ---
if __name__ == "__main__":
    station_data = generate_stations(NUM_STATIONS_TO_GENERATE)
    
    # Save both files
    save_as_json(station_data, OUTPUT_JSON_FILE)
    save_as_csv(station_data, OUTPUT_CSV_FILE)