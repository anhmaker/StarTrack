import os
import requests
from typing import Dict, Any

NASA_API_URL = "https://api.nasa.gov/planetary/apod"


class ApodError(Exception):
    """Safe error class that hides sensitive details from users."""
    pass


class ApodNotFoundError(ApodError):
    """APOD not available for the requested date."""
    pass


class ApodServiceUnavailableError(ApodError):
    """NASA API is temporarily unavailable."""
    pass


def fetch_apod_from_nasa(date: str) -> Dict[str, Any]:
    """Fetch APOD data directly from NASA API."""
    api_key = os.environ.get('NASA_API_KEY', 'DEMO_KEY')
    
    params = {
        'api_key': api_key,
        'date': date
    }
    
    try:
        response = requests.get(NASA_API_URL, params=params, timeout=30)
        
        if response.status_code == 404:
            # Log for debugging (server-side only)
            print(f"[APOD] No data available for date: {date}")
            raise ApodNotFoundError("The future hasn't arrived yet, but we'll get there.")
        
        if response.status_code == 400:
            print(f"[APOD] Bad request for date: {date}")
            raise ApodError("Invalid request. Please check the date format.")
        
        if response.status_code == 403:
            print(f"[APOD] API key issue")
            raise ApodServiceUnavailableError("Service temporarily unavailable. Please try again later.")
        
        if response.status_code >= 500:
            print(f"[APOD] NASA API error: {response.status_code}")
            raise ApodServiceUnavailableError("NASA API is currently unavailable. Please try again later.")
        
        response.raise_for_status()
        
    except requests.exceptions.Timeout:
        print(f"[APOD] Request timeout for date: {date}")
        raise ApodServiceUnavailableError("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        print(f"[APOD] Connection error")
        raise ApodServiceUnavailableError("Could not connect to NASA API. Please check your internet connection.")
    except requests.exceptions.HTTPError as e:
        # Log full error for debugging (server-side)
        print(f"[APOD] HTTP error: {e}")
        raise ApodServiceUnavailableError("An error occurred while fetching data. Please try again later.")
    
    data = response.json()
    
    return {
        'date': data.get('date'),
        'title': data.get('title'),
        'explanation': data.get('explanation'),
        'url': data.get('url'),
        'hdurl': data.get('hdurl'),
        'media_type': data.get('media_type', 'image')
    }


def get_apod_data(date: str) -> Dict[str, Any]:
    """Get APOD data with MinIO caching."""
    from app.storage.minio_client import (
        check_cached_data,
        get_cached_json,
        save_json,
        download_and_save_image
    )
    
    # Check cache first
    if check_cached_data(date):
        cached = get_cached_json(date)
        if cached:
            # Return cached data with local storage URLs
            return {
                **cached,
                'url': f'/storage/image/{date}',
                'hdurl': f'/storage/image/{date}/hd' if cached.get('hdurl') else None,
                'cached': True
            }
    
    # Fetch from NASA API
    data = fetch_apod_from_nasa(date)
    
    # Cache the data if it's an image
    if data.get('media_type') == 'image':
        try:
            # Save metadata
            save_json(date, data)
            
            # Download and save regular image
            if data.get('url'):
                download_and_save_image(date, data['url'], hd=False)
            
            # Download and save HD image if available
            if data.get('hdurl'):
                download_and_save_image(date, data['hdurl'], hd=True)
            
            # Return with local storage URLs
            return {
                **data,
                'url': f'/storage/image/{date}',
                'hdurl': f'/storage/image/{date}/hd' if data.get('hdurl') else None,
                'cached': True
            }
        except Exception as e:
            print(f"Caching failed: {e}")
            # Fall through to return original data
    
    # Return original data (for videos or if caching fails)
    return {**data, 'cached': False}

