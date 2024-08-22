import requests
from config import FOURSQUARE_API_KEY, OPENWEATHERMAP_API_KEY

def get_coordinates(place_name):
    url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
    headers = {
        'User-Agent': 'RealEstate/1.0 (adityak8340@gmail.com)'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = round(float(data[0]['lat']), 2)
                longitude = round(float(data[0]['lon']), 2)
                return latitude, longitude
        return None
    except requests.RequestException:
        return None

def get_nearby_projects(lat, lon):
    url = f"https://api.foursquare.com/v3/places/nearby?ll={lat}%2C{lon}&limit=50"
    headers = {
        "accept": "application/json",
        "Authorization": FOURSQUARE_API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            nearby_projects = []
            for result in json_data.get('results', []):
                project = {
                    'name': result.get('name', 'Unknown'),
                    'distance': result.get('distance', 'Unknown'),
                    'categories': ', '.join(category['name'] for category in result.get('categories', [])),
                    'address': result.get('location', {}).get('address', 'Unknown'),
                    'postcode': result.get('location', {}).get('postcode', 'Unknown'),
                    'country': result.get('location', {}).get('country', 'Unknown'),
                    'developer_reputation': result.get('closed_bucket', 'Unknown')
                }
                if 'Residential Building' in project['categories']:
                    nearby_projects.append(project)
            return nearby_projects
        return None
    except requests.RequestException:
        return None

def get_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["list"][0]["main"]["aqi"]
        return None
    except requests.RequestException:
        return None

def get_nearby_facilities(lat, lon, categories):
    facilities = []
    for category in categories:
        url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&categories={category}&limit=10"
        headers = {
            "accept": "application/json",
            "Authorization": FOURSQUARE_API_KEY
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                facilities.extend(response.json().get('results', []))
        except requests.RequestException:
            pass
    return facilities