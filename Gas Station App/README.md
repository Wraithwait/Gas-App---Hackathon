# Gas Station Finder

A Python prototype application that helps you find nearby gas stations with price comparisons for different fuel types (E85, 87, 89, 91).

## Features

- **Location-based search**: Enter your address to get your current location
- **Multiple fuel types**: Compare prices for E85, Regular 87, Super 89, and Premium 91
- **Flexible sorting**: Sort by closest, cheapest, gas type, or brand
- **Brand filtering**: Filter results by specific gas station brands
- **Distance calculation**: Shows distance from your location to each station

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- requests
- geopy

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python gas_station_finder.py
```

2. Enter your address in the location field and click "Get Location"
3. Choose your sorting preferences (closest, cheapest, gas type, or brand)
4. Optionally filter by gas type or brand
5. Click "Find Gas Stations" to see results

## Note

This is a prototype application using mock data. In a production version, you would integrate with real gas station APIs to get current prices and locations.

## Mock Data

The application currently uses mock data for demonstration purposes. The mock data includes:
- Shell, Exxon, BP, Chevron, Mobil, Speedway, and 7-Eleven stations
- Sample prices for E85, 87, 89, and 91 octane fuels
- Locations around New York City area




