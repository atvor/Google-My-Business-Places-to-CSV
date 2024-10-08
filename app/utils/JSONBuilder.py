import json
import math


def decimal_range(x, y, jump, round_to):
	"""Helper function to yield decimal values within a range."""
	while x < y:
		yield round(x, round_to)
		x += jump


def generate_points(lat_start,
                    lat_to,
                    lon_start,
                    lon_to,
                    step=500,
                    round_to=6,
                    overlap_factor=0.9):
	"""Generates a grid of latitude and longitude points based on the step and overlap factor."""
	lat_step = step / 111000 * overlap_factor  # Step size in degrees for latitude
	lng_step = step / (111000 * math.cos(
			math.radians(lat_start))) * overlap_factor  # Step size for longitude

	lat = list(decimal_range(lat_start, lat_to, lat_step, round_to))
	lon = list(decimal_range(lon_start, lon_to, lng_step, round_to))

	# Ensure that at least one point is generated if ranges are too small
	if not lat:
		lat = [round(lat_start, round_to)]
	if not lon:
		lon = [round(lon_start, round_to)]

	return [(lat_el, lon_el) for lat_el in lat for lon_el in lon]


def bulk_places_to_json(point, places, place_type, json_path):
	"""Writes the places data to a JSON file, updating the existing file if it exists."""
	new_record = {
		f"{place_type} - {point[0]}, {point[1]}": {
			'places': places or {},
			'place_type': place_type,
			'latitude': point[0],
			'longitude': point[1],
			'total': len(places)
		}}

	try:
		# Try to read and update existing JSON file
		with open(json_path, 'r+', encoding='utf-8') as file:
			try:
				data = json.load(file)
			except json.JSONDecodeError:
				data = {}
			data.update(new_record)
			file.seek(0)
			json.dump(data, file, indent=4)
			file.truncate()
	except FileNotFoundError:
		# If file doesn't exist, create a new one
		with open(json_path, 'w', encoding='utf-8') as file:
			json.dump(new_record, file, indent=4)
			print('Created a new JSON file')

	# Reload the updated JSON data
	with open(json_path, 'r', encoding='utf-8') as file:
		return json.load(file)


def remove_duplicates(data):
	"""Removes duplicate entries by googleMapsUri."""
	unique_uris = set()  # Track seen URIs globally
	cleaned_data = {}  # Dictionary to store cleaned entries

	for key, value in data.items():
		if isinstance(value, list):  # Process lists only
			unique_entries = []
			for entry in value:
				if isinstance(entry, dict):  # Ensure entry is a dictionary
					uri = entry.get("googleMapsUri")
					if uri and uri not in unique_uris:
						unique_entries.append(entry)  # Add unique entry
						unique_uris.add(uri)  # Mark URI as seen
			cleaned_data[key] = unique_entries  # Update list with cleaned entries
		else:
			cleaned_data[key] = value  # Preserve non-list items as they are

	return cleaned_data  # Return cleaned dictionary
