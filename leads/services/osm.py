import requests

OSM_URL = "https://nominatim.openstreetmap.org/search"
REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"

def geocode_address(address):
    """Convert address → lat/lon using OSM"""
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    response = requests.get(OSM_URL, params=params, headers={"User-Agent": "bizfinder/1.0"})
    if response.status_code == 200 and response.json():
        return response.json()[0]
    return {"error": "No result"}

def reverse_geocode(lat, lon):
    """Convert lat/lon → full address"""
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json"
    }
    response = requests.get(REVERSE_URL, params=params, headers={"User-Agent": "bizfinder/1.0"})
    if response.status_code == 200:
        return response.json()
    return {"error": "No result"}