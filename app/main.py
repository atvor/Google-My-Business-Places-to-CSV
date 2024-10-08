import asyncio
import concurrent.futures
import json
import os
import time

import folium

from app.MapsAPI import MapsAPI
from app.utils.CSVBuilder import convert_json_to_csv
from app.utils.JSONBuilder import generate_points, bulk_places_to_json, remove_duplicates


start_time = time.perf_counter()


async def fetch_places(maps_api, place_type, point, radius):
	loop = asyncio.get_running_loop()  # Get the current running loop
	# Run the synchronous place_request in a thread pool
	with concurrent.futures.ThreadPoolExecutor() as executor:
		data = await loop.run_in_executor(
				executor, maps_api.place_request, place_type, point[0], point[1], radius
		)

		if data is None:
			print("No data returned, retrying after 60 seconds.")
			await asyncio.sleep(60)

		return data, place_type, point


async def main():
	# ---------------------------------- INPUT ---------------------------------------
	lat_min, lat_max = 50.43, 50.45
	lng_min, lng_max = 30.50, 30.54
	radius = 5000
	place_types = ["accounting", "lawyer", "real_estate_agency"]

	output_prefix = f'{lat_min}-{lat_max}x{lng_min}-{lng_max}_{radius}'
	output_json_path = f'output/{output_prefix}_places.json'
	output_csv_path = f'output/{output_prefix}_places.csv'
	output_html_map_path = 'output/{place_type}_{prefix}_search_coverage_map.html'

	num_workers = os.cpu_count() * 5
	print(f"Number of workers: {num_workers}")

	maps_api = MapsAPI()
	max_requests_per_minute = 600
	request_number = 0

	# Generate points
	points = generate_points(lat_start=lat_min,
	                         lat_to=lat_max,
	                         lon_start=lng_min,
	                         lon_to=lng_max,
	                         step=radius * 2,
	                         overlap_factor=0.705)

	print(points)
	print(f"points amount: {len(points)}")

	color = ['blue', 'white', 'red', 'green', 'black', 'purple', 'brown']
	map_center_lat = (lat_min + lat_max) / 2
	map_center_lng = (lng_min + lng_max) / 2

	found_places = 0

	for place_type in place_types:
		map_obj = folium.Map(location=[map_center_lat, map_center_lng], zoom_start=14)
		tasks = []  # Store tasks for concurrent execution
		i = 0

		for point in points:
			i += 1

			folium.Circle(
					location=point,
					radius=radius,  # Radius in meters
					color='blue',
					fill=True,
					fill_color=color[i % len(color)],
					fill_opacity=0.5,
					tooltip=f'<b>{i}</b>'
			).add_to(map_obj)

			task = fetch_places(maps_api, place_type, point, radius)
			tasks.append(task)

			request_number += 1
			max_requests_per_minute -= 1

			# If the number of requests reaches the limit, wait for the rate limit reset
			if not max_requests_per_minute:
				print("Rate limit reached. Waiting for a minute...")
				await asyncio.sleep(60)  # Wait for the full minute
				request_number = 0

		# Run all tasks concurrently and gather results
		results = await asyncio.gather(*tasks)

		# Process results
		for result in results:
			data, place_type, point = result

			if data:
				places = data.get('places', [])
				found_places += len(places)
				print(f"Found {len(places)} places - {place_type} {point}. ")
				bulk_places_to_json(point, places, place_type, output_json_path)

				for place in places:
					lat, lng = place['location']['latitude'], place['location']['longitude']
					folium.Marker(
							location=[lat, lng],
							popup=f"{place['displayName']['text']}\n <a>{place['googleMapsUri']}</a>",
							tooltip=f"<b>{place['displayName']['text']}</b>"
					).add_to(map_obj)

		# Save the map to an HTML file to visualize
		map_coverage_fn = output_html_map_path.format(place_type=place_type, prefix=output_prefix)
		map_obj.save(map_coverage_fn)
		print(f'saved in {map_coverage_fn}')

	# After gathering all data, remove duplicates and convert to CSV
	with open(output_json_path, 'r', encoding='utf-8') as json_file:
		data = json.load(json_file)
		cleaned_data = remove_duplicates(data)
		unique_places = convert_json_to_csv(json_data=cleaned_data, csv_path=output_csv_path)

	print(f'requests: {request_number} | '
	      f'points: {len(points)} | '
	      f'found: {found_places} | '
	      f'unique: {unique_places} | '
	      f'{round(time.perf_counter() - start_time, 1)} sec.')


if __name__ == "__main__":
	asyncio.run(main())
