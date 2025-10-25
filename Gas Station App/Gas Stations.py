import json
import csv
import random

# --- Configuration ---
OUTPUT_JSON_FILE = 'stations.json'
OUTPUT_CSV_FILE = 'stations.csv'
# ---------------------

# A dictionary to assign price modifiers to brands from your list.
# Unknown brands (like "Gas") get a 0.0 modifier.
BRAND_PREMIUMS = {
    "Shell": 0.35,
    "Arco": -0.10,
    "Chevron": 0.40,
    "Valero": 0.10,
    "Sinclair": 0.05,
    "76": 0.25,
    "Mobil": 0.20,
    "Circle K": 0.0,
    "Speedway Express": 0.0,
    "Chevron G & M": 0.40,
    "Chevron Extra Mile": 0.40,
    "Speedway": 0.0,
    "G & M Oil": 0.0,
    "AM/PM": -0.10,
    "Costco Gas Station": -0.20,
    "G & M Food Mart": 0.0,
    "Gas": 0.0 # Generic "Gas" brand
}


# This list contains all 43 stations you provided,
# with their latitude and longitude added.
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
    """
    Generates data for the predefined list of stations.
    """
    # This will be the final JSON object, with station IDs as keys
    stations_output = {}
    
    # Base price for "average" regular gas in the area
    area_base_price = random.uniform(4.80, 5.10)
    
    # Loop over the predefined station list
    for i, station_def in enumerate(STATION_DEFINITIONS):
        
        # Create a zero-padded ID, e.g., OC-001, OC-002...
        station_id = f"OC-{i+1:03d}"
        brand = station_def['brand']
        
        # Get premium, default to 0.0 if brand not in our list
        premium = BRAND_PREMIUMS.get(brand, 0.0)
        
        # Add a small random amount per-station
        station_randomness = random.uniform(-0.05, 0.05)
        
        # --- Generate Prices ---
        price_reg = round(area_base_price + premium + station_randomness, 2)
        price_mid = round(price_reg + 0.20, 2)
        price_prem = round(price_reg + 0.40, 2)
        
        # --- Create final station object ---
        station_data = {
            "station_id": station_id,
            "brand_name": brand,
            "address": {
                "street": station_def['street'],
                "city": station_def['city'],
                "state": "CA",
                "zip_code": station_def['zip']
            },
            "location": {
                "latitude": station_def['lat'],
                "longitude": station_def['lon']
            },
            "prices": {
                "regular": price_reg,
                "midgrade": price_mid,
                "premium": price_prem,
                # 70% chance of having diesel
                "diesel": round(price_reg + 0.60, 2) if random.random() < 0.7 else None,
                # 25% chance of having E85
                "e85": round(price_reg - 0.50, 2) if random.random() < 0.25 else None
            },
            # Generate a fake timestamp from the "past" 24 hours
            "last_updated": f"2025-10-24T{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}Z"
        }
        
        # Add to the main dictionary using the ID as the key
        stations_output[station_id] = station_data
        
    return stations_output

def save_as_json(stations_dict, filename):
    """Saves the station dictionary as a JSON file."""
    with open(filename, 'w') as f:
        # The stations_dict is already in the format { "OC-001": {...}, ... }
        json.dump(stations_dict, f, indent=2)
    print(f"Successfully generated {filename}")

def save_as_csv(stations_dict, filename):
    """Saves the station data as a CSV file."""
    if not stations_dict:
        return
        
    headers = [
        'station_id', 'brand_name', 'street_address', 'city', 'state', 'zip_code',
        'latitude', 'longitude', 'regular_price', 'midgrade_price', 
        'premium_price', 'diesel_price', 'e85_price', 'last_updated'
    ]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        # We iterate over the .values() of the dictionary to get the list
        for station in stations_dict.values():
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
    station_data_dict = generate_station_data()
    
    # Save both files
    save_as_json(station_data_dict, OUTPUT_JSON_FILE)
    save_as_csv(station_data_dict, OUTPUT_CSV_FILE)