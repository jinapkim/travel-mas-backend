import json
import requests


def FindLatLong(location):
        api_key = 'AIzaSyCBWhzr0B8_CSuIe7WoXXsqsRGzT5K5_fk'

        # Call the Google Maps Find Place API to find the place_id to use for the Geocoding API
        url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input={}&types=geocode&key={}".format(location, api_key)

        payload={}
        headers = {}

        response = requests.get(url, headers=headers, data=payload)

        jresponse = json.loads(response.text)
        location_id = jresponse["predictions"][0]['place_id']

        # Call the Google Maps Geocoding API to get the GPS coordinates
        url = "https://maps.googleapis.com/maps/api/geocode/json?place_id={}&key={}".format(location_id, api_key)

        payload={}
        headers = {}

        response = requests.get(url, headers=headers, data=payload)

        jresponse = json.loads(response.text)
        geolocation = jresponse["results"][0]["geometry"]["location"]
        geolocation_string = str(geolocation["lat"]) + ", " + str(geolocation["lng"])
        
        return geolocation_string
