import os

import requests


class MapsAPI:
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

    # https://developers.google.com/maps/documentation/places/web-service/nearby-search
    GOOGLE_PLACES_API_PATH = 'https://places.googleapis.com/v1/places:searchNearby'
    # autocomple request: https://places.googleapis.com/v1/places:autocomplete

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
                  'places.formattedAddress']

    # places_types https://developers.google.com/maps/documentation/places/web-service/place-types


    def __init__(self,
                 api_key='',
                 api_path=''):
        self.GOOGLE_MAPS_API_KEY = api_key if api_key else self.GOOGLE_MAPS_API_KEY
        self.GOOGLE_PLACES_API_PATH = api_path if api_path else self.GOOGLE_PLACES_API_PATH


    def place_request(self,
                      places_types,     # https://developers.google.com/maps/documentation/places/web-service/place-types
                      latitude,
                      longitude,
                      radius,       # meters
                      max_result_len=10,
                      enable_mask=True,
                      field_mask=''):

        field_mask = field_mask if field_mask else self.FIELD_MASK

        return requests.post(
            url=self.GOOGLE_PLACES_API_PATH,
            json={
                "includedTypes": places_types,
                "maxResultCount": max_result_len,
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
                # 'X-Goog-FieldMask': '*',  # use to get all fields
                # 'X-Goog-FieldMask': ','.join(self.field_mask),
            }
        )
