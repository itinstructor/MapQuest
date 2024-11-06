"""
    Name: mapquest_cli.py
    Author:
    Created:
    Purpose: OOP console app
    Geocode with mapquest williamloring@hotmail.com wloring 99FloatBeans99!
    Returns map link of location
    lat: 41.89208 lon: -103.67189
"""

import requests
from api_key import API_KEY, GEOCODE_ENDPOINT

location = input("Enter location by st address: ")

params = {
    "key": API_KEY,
    "location": location,
    "maxResults": 1
}

geo_response = requests.get(
    GEOCODE_ENDPOINT,
    params=params
)

geo_coord = geo_response.json()

print(geo_coord)

latitude = geo_coord["results"][0]["locations"][0]["latLng"]["lat"]
longitude = geo_coord["results"][0]["locations"][0]["latLng"]["lng"]

print(f"lat: {latitude} lng: {longitude}")
