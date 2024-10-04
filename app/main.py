from app.MapsAPI import MapsAPI
from app.utils.CSVBuilder import convert_json_to_csv
from app.utils.JSONBuilder import generate_points, bulk_points_to_json

# ---------------------------------- INPUT ---------------------------------------
output_json_path = 'output/places.json'
output_csv_path = 'output/places.csv'

latitude_start = 42.35
latitude_to = 42.37
longitude_start = -71.08
longitude_to = -71.05

my_radius = 555
my_step = 0.005
my_lat_cf = 1
my_lon_cf = 1.6

# # https://developers.google.com/maps/documentation/places/web-service/place-types
my_places_types = ["accounting"]

# ----------------------------------- OUTPUT -------------------------------------------
mapsAPI = MapsAPI()

# generate coordinates
points = generate_points(lat_start=latitude_start,
                         lat_to=latitude_to,
                         lon_start=longitude_start,
                         lon_to=longitude_to,
                         step=my_step,
                         lat_cf=my_lat_cf,
                         lon_cf=my_lon_cf)

print(points)
print(f"points amount: {len(points)}")

data = bulk_points_to_json(points,
                           mapsAPI,
                           places_types=my_places_types,
                           radius=my_radius,
                           json_path=output_json_path,
                           max_result_len=20)

convert_json_to_csv(json_data=data, csv_path=output_csv_path)
