import json
import csv


def convert_json_to_csv(json_data, csv_path):
    # Prepare the CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Write the headers
        writer.writerow([
            "coordinate",
            "types",
            "websiteUri",
            "nationalPhoneNumber",
            "internationalPhoneNumber",
            "formattedAddress",
            "displayName",
            "rating",
            "userRatingCount",
            "googleMapsUri"
        ])

        # Iterate over each coordinate and its associated businesses
        for coordinate, businesses in json_data.items():
            if businesses:  # Check if there are businesses at this coordinate
                for business in businesses:
                    # Extract business details, provide defaults if missing
                    types = ', '.join(business.get('types', []))
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
                        coordinate,
                        types,
                        websiteUri,
                        nationalPhoneNumber,
                        internationalPhoneNumber,
                        formattedAddress,
                        displayName,
                        rating,
                        userRatingCount,
                        googleMapsUri
                    ])
