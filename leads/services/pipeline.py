from .search import search_businesses
from .linkedin import fetch_linkedin_company
from .osm import geocode_address

def enrich_businesses(query, country):
    """
    Full pipeline:
    - Get businesses (RapidAPI / OSM)
    - Add LinkedIn & OSM enrichment
    """
    base_results = search_businesses(query, country)
    enriched = []

    for biz in base_results:
        name = biz.get("name")
        address = biz.get("address")

        # LinkedIn enrichment
        #linkedin_info = fetch_linkedin_company(name)

        # OSM geocode (lat/lon)
        osm_info = geocode_address(address)

        enriched.append({
            **biz,  # keep name, address, website, etc.
            #"linkedin": linkedin_info,
            "osm": osm_info,
        })
    return enriched