import json
import time


def generate_points(lat_start,
                    lat_to,
                    lon_start,
                    lon_to,
                    step=0.005,
                    lat_cf=1,
                    lon_cf=1,
                    round_to=4):
    def decimal_range(x, y, jump):
        while x < y:
            yield round(x, round_to)
            x += jump

    lat = list(decimal_range(lat_start, lat_to, step * lat_cf))
    lon = list(decimal_range(lon_start, lon_to, step * lon_cf))

    points = []
    for lat_el in lat:
        for lon_el in lon:
            points.append((lat_el, lon_el))

    return points


def bulk_points_to_json(points,
                        mapsAPI,
                        places_types,
                        radius,
                        json_path,
                        max_result_len=20,
                        request_per_minute=600):
    request_number = 0
    for point in points:
        if request_number >= request_per_minute:
            print('reached request per minute limit')
            time.sleep(60)
            request_number = 0

        request_places = mapsAPI.place_request(
            places_types=places_types,
            latitude=point[0],
            longitude=point[1],
            radius=radius,
            max_result_len=max_result_len)  # max 20

        request_number += 1
        print(f"request {request_number}: {request_places}")

        response_dict = request_places.json()
        places = response_dict.get('places')

        # ------------------------- write JSON
        if places:
            print(f"{point[0]}, {point[1]} - {len(response_dict['places'])}")
            new_record = {f"{point[0]}, {point[1]}": response_dict['places']}  # Whatever your structure is
        else:
            print(response_dict)
            new_record = {f"{point[0]}, {point[1]}": {}}

        try:
            with open(json_path, mode='r') as file:
                data = json.load(file)
                data.update(new_record)
            with open(json_path, mode='w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"error: {e}")
            with open(json_path, mode='w') as file:
                json.dump(new_record, file, indent=4)

    # Load the JSON data from a file
    with open(json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        return data
