import json

from MapsAPI import MapsAPI
from utils.CSVBuilder import write_dict_to_csv

latitude = 37.7937
longitude = -122.3965
radius = 500.0      # meters
places_types = ["accounting"]

mapsAPI = MapsAPI()

request_places = mapsAPI.place_request(
    places_types=places_types,
    latitude=latitude,
    longitude=longitude,
    radius=radius,
    max_result_len=20,
)


print(request_places)

response_dict = request_places.json()
places = response_dict.get('places')

if places:
    print(len(response_dict['places']))

    write_dict_to_csv(response_dict['places'], 'output/places.csv')

    with open('output/data.json', 'w') as f:
        json.dump(response_dict, f, indent=4)

else:
    print(response_dict)
