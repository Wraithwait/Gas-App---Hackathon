# Google Places API Integration Setup

This guide shows you how to integrate Google Places API for real-time gas station data and travel information.

## 🔑 **Getting Your API Key**

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable billing (required for Places API)

### 2. Enable Required APIs
Enable these APIs in your project:
- **Places API** - For gas station data
- **Directions API** - For travel time and routes
- **Geocoding API** - For address conversion (if not using geopy)

### 3. Create API Key
1. Go to "Credentials" in Google Cloud Console
2. Click "Create Credentials" → "API Key"
3. Copy your API key
4. (Optional) Restrict the key to specific APIs and IPs for security

## ⚙️ **Setup Instructions**

### 1. Set Environment Variable
```bash
# Set your API key
export GOOGLE_PLACES_API_KEY="your_actual_api_key_here"

# Or create a .env file
echo "GOOGLE_PLACES_API_KEY=your_actual_api_key_here" > .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python3 gas_station_finder_web.py
```

## 🚀 **New Features with Google Places API**

### Real-Time Gas Station Data
- **Live Results**:** Actual gas stations from Google's database
- **Ratings & Reviews**: Star ratings and review counts
- **Business Status**: Open/closed status in real-time
- **Photos**: Station photos when available
- **Detailed Info**: Phone numbers, websites, addresses

### Travel Information
- **Travel Time**: Real driving time with traffic
- **Distance**: Accurate road distance
- **Directions**: Step-by-step navigation
- **Multiple Modes**: Driving, walking, cycling, transit

### Enhanced UI Features
- **Click Stations**: Click any station for detailed info
- **Get Directions**: One-click directions to any station
- **Real-Time Status**: See which stations are open
- **Photos**: View station photos
- **Ratings**: See Google ratings and reviews

## 📊 **API Usage & Costs**

### Google Places API Pricing (as of 2024)
- **Places Nearby Search**: $32 per 1,000 requests
- **Place Details**: $17 per 1,000 requests  
- **Directions API**: $5 per 1,000 requests
- **Geocoding**: $5 per 1,000 requests

### Cost Optimization Tips
1. **Cache Results**: Store results for 15-30 minutes
2. **Limit Radius**: Use smaller search radius when possible
3. **Batch Requests**: Combine multiple API calls
4. **Free Tier**: $200/month free credit for new users

## 🔧 **Configuration Options**

### Search Radius
```python
# In google_places_integration.py
stations = service.search_gas_stations(lat, lon, radius=5000)  # 5km radius
```

### Filter Options
```python
# Filter by rating and open status
stations = service.search_with_filters(
    lat, lon, 
    min_rating=4.0,  # Only 4+ star stations
    open_now=True    # Only open stations
)
```

### Travel Modes
```python
# Different travel modes
travel_info = service.get_travel_time(
    origin, destination, 
    mode='driving'  # or 'walking', 'bicycling', 'transit'
)
```

## 🛡️ **Security Best Practices**

### API Key Security
1. **Restrict APIs**: Only enable required APIs
2. **IP Restrictions**: Limit to your server IPs
3. **HTTP Referrers**: Restrict to your domain
4. **Environment Variables**: Never commit API keys to code

### Rate Limiting
```python
# Add rate limiting to prevent API abuse
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Implement rate limiting logic
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 🐛 **Troubleshooting**

### Common Issues

1. **"API key not valid"**
   - Check if API key is correct
   - Verify APIs are enabled in Google Cloud Console
   - Check billing is enabled

2. **"Quota exceeded"**
   - Check API usage in Google Cloud Console
   - Implement caching to reduce API calls
   - Consider upgrading billing plan

3. **"No results found"**
   - Try larger search radius
   - Check if location is valid
   - Verify gas stations exist in that area

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 **Performance Optimization**

### Caching Strategy
```python
import redis
from datetime import datetime, timedelta

# Cache gas station results for 30 minutes
def get_cached_stations(lat, lon, radius):
    cache_key = f"stations_{lat}_{lon}_{radius}"
    cached = redis.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # Fetch from API and cache
    stations = api_search(lat, lon, radius)
    redis.setex(cache_key, 1800, json.dumps(stations))  # 30 min cache
    return stations
```

### Batch Processing
```python
# Process multiple locations at once
def batch_search_locations(locations):
    results = []
    for lat, lon in locations:
        stations = search_gas_stations(lat, lon)
        results.extend(stations)
    return results
```

## 🎯 **Next Steps**

1. **Set up your API key** using the instructions above
2. **Test the integration** with a small search radius
3. **Monitor API usage** in Google Cloud Console
4. **Implement caching** to reduce costs
5. **Add error handling** for production use

## 📞 **Support**

- **Google Places API Docs**: https://developers.google.com/maps/documentation/places/web-service
- **Google Cloud Console**: https://console.cloud.google.com/
- **API Status**: https://status.cloud.google.com/


