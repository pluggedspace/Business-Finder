import requests
from django.conf import settings

RAPIDAPI_HOST = "maps-data.p.rapidapi.com"
RAPIDAPI_KEY = settings.RAPIDAPI_KEY


def geocode_region_osm(country):
    """
    Convert country/place name into a standardized country code using OSM Nominatim
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": country,
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    response = requests.get(url, params=params, headers={"User-Agent": "business-finder"})
    if response.status_code == 200 and response.json():
        item = response.json()[0]
        return {
            "country": item.get("address", {}).get("country_code", "us")
        }
    # fallback → US
    return {"country": "us"}


def search_businesses_rapidapi(query, country):
    """
    Search businesses using RapidAPI Maps Data
    """
    geo = geocode_region_osm(country)

    url = f"https://{RAPIDAPI_HOST}/searchmaps.php"
    querystring = {
        "query": query,
        "limit": "20",
        "lang": "en",
        "country": geo["country"],   # ✅ use country only
        "zoom": "13"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)
    print("🔎 RapidAPI raw response:", response.text)  # DEBUG

    if response.status_code == 200:
        try:
            data = response.json()
        except Exception:
            return []

        if not data or not isinstance(data.get("data"), list):
            return []

        results = []
        for item in data["data"]:
            results.append({
                "name": item.get("name"),
                "category": ", ".join(item.get("types", [])) if item.get("types") else None,
                "address": item.get("full_address"),
                "website": item.get("website") or "",
                "phone": item.get("phone_number") or "",
                "rating": item.get("rating"),
                "reviews": item.get("review_count"),
                "lat": item.get("latitude"),
                "lng": item.get("longitude"),
                "place_link": item.get("place_link"),
                "photos": item.get("photos", []),
                "source": "rapidapi"
            })
        return results

    return []


def search_businesses_osm(query, country):
    """
    Fallback: Search businesses using OpenStreetMap Nominatim
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{query} {country}",
        "format": "json",
        "addressdetails": 1,
        "limit": 10
    }
    response = requests.get(url, params=params, headers={"User-Agent": "business-finder"})
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data:
            results.append({
                "name": item.get("display_name"),
                "category": query,
                "address": item.get("display_name"),
                "website": "",
                "phone": "",
                "rating": None,
                "reviews": None,
                "lat": item.get("lat"),
                "lng": item.get("lon"),
                "place_link": "",
                "photos": [],
                "source": "osm"
            })
        return results
    return []


def search_businesses(query, country, fallback=False):
    results = search_businesses_rapidapi(query, country)
    if not results and fallback:
        results = search_businesses_osm(query, country)
    return results