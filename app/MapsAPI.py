import os
from typing import Literal

import requests


class MapsAPI:
	GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

	# https://developers.google.com/maps/documentation/places/web-service/nearby-search
	GOOGLE_PLACES_API_PATH = 'https://places.googleapis.com/v1/places:searchNearby'

	# https://developers.google.com/maps/documentation/places/web-service/data-fields
	FIELD_MASK = ['places.displayName.text',
	              'places.primaryTypeDisplayName.text',
	              'places.types',
	              'places.nationalPhoneNumber',
	              'places.internationalPhoneNumber',
	              'places.rating',
	              'places.userRatingCount',
	              'places.googleMapsUri',
	              'places.websiteUri',
	              'places.priceLevel',
	              'places.formattedAddress',
	              'places.location']

	def __init__(self, api_key='', api_path=''):
		self.GOOGLE_MAPS_API_KEY = api_key if api_key else self.GOOGLE_MAPS_API_KEY
		self.GOOGLE_PLACES_API_PATH = api_path if api_path else self.GOOGLE_PLACES_API_PATH

		if not self.GOOGLE_MAPS_API_KEY:
			raise ValueError("API key is required")

	def place_request(self,
	                  place_types: list,
	                  latitude: float,
	                  longitude: float,
	                  radius: int,
	                  max_result_len: int = 20,
	                  enable_mask: bool = True,
	                  field_mask: list = '',
	                  rank_preference: Literal["DISTANCE",
	                  "POPULARITY"] = "DISTANCE"):
		"""
		Sends a request to the Google Places API to retrieve places based on the specified location and criteria.

		Args:
			place_types (list): List of place types to filter (e.g., ['restaurant', 'bank']).
			latitude (float): Latitude of the location.
			longitude (float): Longitude of the location.
			radius (int): Radius in meters to search within.
			max_result_len (int): Maximum number of results to return.
			enable_mask (bool): If True, apply the field mask to the response.
			field_mask (list): Custom field mask to filter the results.
			rank_preference (str): Ranking preference for results ("DISTANCE" or "POPULARITY").

		Returns:
			dict: Parsed JSON response from the API.
		"""
		field_mask = field_mask if field_mask else self.FIELD_MASK

		try:
			response = requests.post(
					url=self.GOOGLE_PLACES_API_PATH,
					json={
						"includedTypes": place_types,
						"maxResultCount": max_result_len,
						"rankPreference": rank_preference,
						"locationRestriction": {
							"circle": {
								"center": {
									"latitude": latitude,
									"longitude": longitude
								},
								"radius": radius  # meters
							}
						}
					},
					headers={
						'Content-Type': 'application/json',
						'X-Goog-Api-Key': self.GOOGLE_MAPS_API_KEY,
						'X-Goog-FieldMask': ','.join(field_mask) if enable_mask else "*"
					}
			)

			response.raise_for_status()  # Raise exception for bad responses
			return response.json()  # Parse and return the JSON response

		except Exception as e:
			print(f"Error during API request: {e}")
			return None
