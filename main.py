import json
import os
import requests

from utils.CSVBuilder import write_dict_to_csv

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

# https://developers.google.com/maps/documentation/places/web-service/nearby-search
GOOGLE_PLACES_API_PATH = 'https://places.googleapis.com/v1/places:searchNearby'
# autocomple request: https://places.googleapis.com/v1/places:autocomplete

# https://developers.google.com/maps/documentation/places/web-service/place-types
places_types = ["accounting"]

# https://developers.google.com/maps/documentation/places/web-service/data-fields
field_mask = ['places.displayName.text',
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

response = requests.post(
    url=GOOGLE_PLACES_API_PATH,
    json={
        "includedTypes": places_types,
        "maxResultCount": 10,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": 37.7937,
                    "longitude": -122.3965},
                "radius": 500.0  # meters
            }
        }
    },
    headers={
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': GOOGLE_MAPS_API_KEY,
        # 'X-Goog-FieldMask': '*',  # use to get all fields
        'X-Goog-FieldMask': ','.join(field_mask),
    }
)

print(response)
response_dict = response.json()
places = response_dict.get('places')

if places:
    print(len(response_dict['places']))

    write_dict_to_csv(response_dict['places'], 'out/places.csv')

    with open('out/data.json', 'w') as f:
        json.dump(response_dict, f, indent=4)

else:
    print(response_dict)
