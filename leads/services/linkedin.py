import requests
import time
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

RAPIDAPI_KEY = settings.RAPIDAPI_KEY
LINKEDIN_URL = "https://linkedin-data-api.p.rapidapi.com/get-company-details"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
}

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(429, 500, 502, 503, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def fetch_linkedin_company(company_name):
    """Fetch company info from LinkedIn via RapidAPI with retry logic"""
    try:
        session = requests_retry_session()
        response = session.get(
            LINKEDIN_URL,
            headers=HEADERS,
            params={"username": company_name},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            return {"error": f"API returned status code: {response.status_code}"}
            
    except Exception as e:
        return {"error": str(e)}