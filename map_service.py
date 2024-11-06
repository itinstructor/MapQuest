"""
    Name: map_service.py
    Author:
    Created:
    Purpose: MapQuest service class to retrieve maps of location
    15,000 requests per month
"""
import requests
from PIL import Image
from io import BytesIO
from api_key import API_KEY, GEOCODE_ENDPOINT, MAP_ENDPOINT


class MapService:
    """
    A service class that handles all interactions with the MapQuest API.
    This includes geocoding locations and retrieving static map images.
    """

    def __init__(self):
        # Default dimensions for the map image
        self.width = 800
        self.height = 600

    # ----------------------- GEOCODE LOCATION --------------------------- #
    def geocode_location(self, location):
        """
        Convert a location string into geographical coordinates 
        and address details.

        Args:
            location (str): A location string (e.g., "New York, NY" or
            "1600 Pennsylvania Ave")

        Returns:
            dict: Location data including coordinates and address components
                 Returns None if location cannot be found

        Raises:
            Exception: If the API request fails or returns an error
        """

        # Parameters for the geocoding request
        params = {
            'key': API_KEY,
            'location': location,
            'maxResults': 1  # We only need the best match
        }

        try:
            # Make the API request
            response = requests.get(
                GEOCODE_ENDPOINT,
                params=params
            )

            # Raise an exception for bad status codes
            response.raise_for_status()

            # Parse the JSON response into a dictionary
            data = response.json()

            # Check if we got any results
            if data['results'] and data['results'][0]['locations']:
                location_data = data['results'][0]['locations'][0]
                lat_lng = location_data['latLng']

                # Return structured location data
                return {
                    'latitude': lat_lng['lat'],
                    'longitude': lat_lng['lng'],
                    'street': location_data.get('street', 'N/A'),
                    'city': location_data.get('adminArea5', 'N/A'),
                    'state': location_data.get('adminArea3', 'N/A'),
                    'postal_code': location_data.get('postalCode', 'N/A')
                }
            return None

        except requests.exceptions.RequestException as e:
            raise Exception(f"Geocoding failed: {str(e)}")

# ------------------------- GET STATIC MAP ------------------------------- #
    def get_static_map(self, location, zoom, map_type):
        """
        Retrieve a static map image for a given location.

        Args:
            location (str): Location string to map
            zoom (str/int): Zoom level (1-20)
            map_type (str): Type of map (map, sat, hyb, light, dark)

        Returns:
            tuple: (PIL.Image, dict) - The map image and location data

        Raises:
            Exception: If the location cannot be found or 
            the map cannot be retrieved
        """

        # Get the coordinates for the location
        location_data = self.geocode_location(location)

        # Check if location was found
        if not location_data:
            raise Exception("Location not found")

        # Create the center point string for the map
        center = f"{location_data['latitude']},{location_data['longitude']}"

        # Parameters for the static map request
        params = {
            'key': API_KEY,
            'center': center,
            'size': f"{self.width},{self.height}",
            'zoom': zoom,
            'locations': center,  # This adds a marker at the location
            'type': map_type,
            'defaultMarker': 'marker-md-3B5998-22407F'  # Custom marker style
        }

        try:
            # Get the map image
            response = requests.get(MAP_ENDPOINT, params=params)

            # Raise an exception for bad status codes
            response.raise_for_status()

            # Convert the response content to a PIL Image
            return Image.open(BytesIO(response.content)), location_data

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch map: {str(e)}")
