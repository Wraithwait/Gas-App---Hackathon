# Gas Station Finder - Setup Guide

## 🚀 Quick Start (Recommended)

### Option 1: Web GUI with Mapbox API (Recommended for Real Data!)
```bash
# Set your Mapbox access token
export MAPBOX_ACCESS_TOKEN="pk.eyJ1Ijoid3JhaXRod2FpdCIsImEiOiJjbWg2cHRiajgwa3N0MmpvbW9mZ2lxeGtqIn0.UXl2DSFjbSSRntzofhFm9g"

# Run the application
python3 gas_station_finder_web.py
```
Then open your browser and go to: **http://localhost:5000**

This provides real-time gas station data and travel information!

### Option 2: Web GUI (Works Immediately - No API Required!)
```bash
python3 gas_station_finder_web.py
```
Then open your browser and go to: **http://localhost:5000**

This provides a beautiful web interface with mock data for testing!

### Option 2: Run the Offline Demo (Works Immediately)
```bash
python3 gas_station_finder_offline.py
```
This version works without internet and demonstrates all features using mock data.

### Option 3: Run the Command-Line Version
```bash
python3 gas_station_finder_cli.py
```
This version includes geocoding but requires internet connectivity.

## 🖥️ GUI Version (Tkinter)

### Prerequisites
The tkinter GUI version requires a system reboot after installation:

1. **Install tkinter** (already done):
   ```bash
   rpm-ostree install python3-tkinter
   ```

2. **Reboot your system**:
   ```bash
   systemctl reboot
   ```

3. **After reboot, run the GUI version**:
   ```bash
   python3 gas_station_finder.py
   ```

## 📋 Available Versions

| Version | Description | Requirements |
|---------|-------------|--------------|
| `gas_station_finder_web.py` | **Web GUI with Mapbox API** | Python 3.7+ + Flask + Mapbox token |
| `gas_station_finder_web.py` | **Web GUI with Mock Data** | Python 3.7+ + Flask only |
| `gas_station_finder_offline.py` | Demo version with mock data | Python 3.7+ only |
| `gas_station_finder_cli.py` | Command-line with geocoding | Python 3.7+ + internet |
| `gas_station_finder.py` | Desktop GUI with Tkinter | Python 3.7+ + tkinter + internet |

## 🧪 Testing the Application

### Test Core Functionality
```bash
python3 gas_station_finder_offline.py
```

### Test with Real Geocoding
```bash
python3 gas_station_finder_cli.py
```

## 🔧 Troubleshooting

### If tkinter is not available:
- Use the offline version: `python3 gas_station_finder_offline.py`
- Use the CLI version: `python3 gas_station_finder_cli.py`

### If geocoding fails:
- Check internet connection
- Use the offline version for testing

### If dependencies are missing:
```bash
pip3 install -r requirements.txt
```

## 📊 Features Demonstrated

✅ **Location-based search** - Enter address to get coordinates  
✅ **Multiple fuel types** - E85, 87, 89, 91 octane prices  
✅ **Distance calculation** - Shows distance from your location  
✅ **Sorting options** - Closest, cheapest, gas type, brand  
✅ **Filtering** - By gas type and brand  
✅ **Clean UI** - Both command-line and GUI interfaces  

## 🎯 Next Steps for Production

1. **Real API Integration**: Replace mock data with real gas station APIs
2. **Database**: Store gas station data locally
3. **Real-time Updates**: Fetch current prices
4. **Mobile App**: Convert to mobile application
5. **User Accounts**: Save favorite locations and preferences

