# Mapbox API Integration Setup

This guide shows you how to integrate Mapbox API for real-time gas station data and travel information.

## 🔑 **Getting Your Access Token**

### 1. Create Mapbox Account
1. Go to [Mapbox](https://www.mapbox.com/)
2. Sign up for a free account
3. Verify your email address

### 2. Get Your Access Token
1. Go to your [Mapbox Account](https://account.mapbox.com/)
2. Navigate to "Access tokens"
3. Copy your default public token
4. (Optional) Create a new token with specific scopes

### 3. Enable Required APIs
Mapbox includes these APIs by default:
- **Geocoding API** - For POI search and address geocoding
- **Directions API** - For travel time and routes
- **Matrix API** - For multiple point calculations

## ⚙️ **Setup Instructions**

### 1. Set Environment Variable
```bash
# Set your access token
export MAPBOX_ACCESS_TOKEN="your_mapbox_access_token_here"

# Or create a .env file
echo "MAPBOX_ACCESS_TOKEN=your_mapbox_access_token_here" > .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python3 gas_station_finder_web.py
```

## 🚀 **New Features with Mapbox API**

### Real-Time Gas Station Data
- **Live POI Search**: Actual gas stations from Mapbox database
- **Distance Calculation**: Accurate distance calculations
- **POI Categories**: Filter by gas station types
- **Address Information**: Formatted addresses for each station

### Travel Information
- **Real Travel Time**: Actual driving time with traffic
- **Accurate Distance**: Road distance calculations
- **Multiple Profiles**: Driving, walking, cycling
- **Route Geometry**: Detailed route information

### Enhanced Features
- **Matrix API**: Calculate travel times to multiple stations at once
- **Geocoding**: Convert addresses to coordinates
- **POI Filtering**: Filter by brand and category
- **Cost Effective**: More affordable than Google Places API

## 📊 **API Usage & Costs**

### Mapbox Pricing (as of 2024)
- **Free Tier**: 50,000 requests/month
- **Geocoding**: $0.50 per 1,000 requests after free tier
- **Directions**: $0.50 per 1,000 requests after free tier
- **Matrix API**: $0.50 per 1,000 requests after free tier

### Cost Comparison
| Feature | Google Places | Mapbox |
|---------|---------------|--------|
| POI Search | $32/1k | $0.50/1k |
| Directions | $5/1k | $0.50/1k |
| Geocoding | $5/1k | $0.50/1k |
| Free Tier | $200 credit | 50k requests |

## 🔧 **Configuration Options**

### Search Radius
```python
# In mapbox_integration.py
stations = service.search_poi(lat, lon, radius=5000)  # 5km radius
```

### Travel Profiles
```python
# Different travel modes
directions = service.get_directions(
    origin, destination, 
    profile='driving'  # or 'walking', 'cycling'
)
```

### POI Types
```python
# Search for different POI types
stations = service.search_poi(lat, lon, poi_type='gas_station')
# Other types: 'restaurant', 'hotel', 'hospital', etc.
```

## 🛡️ **Security Best Practices**

### Access Token Security
1. **Use Environment Variables**: Never hardcode tokens
2. **Token Scoping**: Create tokens with minimal required scopes
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **HTTPS Only**: Always use HTTPS in production

### Rate Limiting
```python
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

1. **"Invalid access token"**
   - Check if access token is correct
   - Verify token has required scopes
   - Ensure token is not expired

2. **"Quota exceeded"**
   - Check API usage in Mapbox account
   - Implement caching to reduce API calls
   - Consider upgrading plan

3. **"No results found"**
   - Try larger search radius
   - Check if location is valid
   - Verify POI type is correct

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

# Cache POI results for 30 minutes
def get_cached_poi(lat, lon, radius):
    cache_key = f"poi_{lat}_{lon}_{radius}"
    cached = redis.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # Fetch from API and cache
    poi = api_search(lat, lon, radius)
    redis.setex(cache_key, 1800, json.dumps(poi))  # 30 min cache
    return poi
```

### Batch Processing
```python
# Use Matrix API for multiple destinations
def get_travel_times_to_stations(origin, stations):
    coordinates = [origin] + [(s['lat'], s['lon']) for s in stations]
    matrix = service.get_matrix(coordinates)
    return matrix
```

## 🎯 **Advanced Features**

### Custom POI Categories
```python
# Search for specific gas station brands
def search_brand_stations(lat, lon, brand):
    stations = service.search_poi(lat, lon, poi_type='gas_station')
    return [s for s in stations if brand.lower() in s['name'].lower()]
```

### Traffic-Aware Routing
```python
# Use driving-traffic profile for real-time traffic
directions = service.get_directions(
    origin, destination, 
    profile='driving-traffic'  # Requires premium plan
)
```

### Batch Geocoding
```python
# Geocode multiple addresses
def batch_geocode(addresses):
    results = []
    for address in addresses:
        coords = service.geocode_address(address)
        results.append({'address': address, 'coordinates': coords})
    return results
```

## 🔄 **Migration from Google Places**

### Key Differences
| Feature | Google Places | Mapbox |
|---------|---------------|--------|
| POI Search | `nearbysearch` | `geocoding` with `types` |
| Place Details | `place/details` | Limited (use search results) |
| Directions | `directions` | `directions` |
| Photos | `place/photo` | Not available |
| Reviews | Included | Not available |

### Migration Steps
1. **Replace API calls** with Mapbox equivalents
2. **Update data structures** to match Mapbox format
3. **Implement caching** for better performance
4. **Add fallback logic** for missing features

## 📞 **Support**

- **Mapbox Docs**: https://docs.mapbox.com/
- **Mapbox Account**: https://account.mapbox.com/
- **API Status**: https://status.mapbox.com/
- **Community**: https://community.mapbox.com/

## 🎯 **Next Steps**

1. **Set up your access token** using the instructions above
2. **Test the integration** with a small search radius
3. **Monitor API usage** in your Mapbox account
4. **Implement caching** to reduce costs
5. **Add error handling** for production use

