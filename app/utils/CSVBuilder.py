import csv


def convert_json_to_csv(json_data, csv_path):
	created_rows = 0

	# Prepare the CSV file
	with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
		writer = csv.writer(csv_file)

		# Write the headers
		writer.writerow([
			"place_type",
			"displayName",
			"websiteUri",
			"nationalPhoneNumber",
			"internationalPhoneNumber",
			"formattedAddress",
			"rating",
			"userRatingCount",
			"googleMapsUri",
			"latitude",
			"longitude",
			"total"
			"types",

		])

		print(json_data.items())
		# Iterate over each coordinate and its associated businesses
		for coordinate, data in json_data.items():
			places, place_type, latitude, longitude, total = data.values()

			if places:  # Check if there are businesses at this coordinate
				for business in places:
					# Extract business details, provide defaults if missing
					types = business.get('types', [])
					websiteUri = business.get('websiteUri', '')
					nationalPhoneNumber = business.get('nationalPhoneNumber', '')
					internationalPhoneNumber = business.get('internationalPhoneNumber', '')
					formattedAddress = business.get('formattedAddress', '')
					displayName = business.get('displayName', {}).get('text', '')
					rating = business.get('rating', '')
					userRatingCount = business.get('userRatingCount', '')
					googleMapsUri = business.get('googleMapsUri', '')

					# Write the row for each business
					writer.writerow([
						place_type,
						displayName,
						websiteUri,
						nationalPhoneNumber,
						internationalPhoneNumber,
						formattedAddress,
						rating,
						userRatingCount,
						googleMapsUri,
						latitude,
						longitude,
						total,
						types
					])

					created_rows += 1

	return created_rows
