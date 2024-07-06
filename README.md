# Google My Business Places to CSV

A simple template to get information about places from Google My Business with Places API and convert it into a CSV file with Pandas

> [!IMPORTANT]
> Setup your .env file with the variable `GOOGLE_MAPS_API_KEY` before you run the script

or you can run it like here 
```bazaar
GOOGLE_MAPS_API_KEY="PUT_YOUR_KEY" python main.py
```

## Customize
### You can change places' types 
https://developers.google.com/maps/documentation/places/web-service/place-types

```bazaar
places_types
```

### Response's fields 
https://developers.google.com/maps/documentation/places/web-service/data-fields

```bazaar
field_mask
```

Learn more about Google Places API: 
https://developers.google.com/maps/documentation/places/web-service/op-overview