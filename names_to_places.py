"""This script retrieves addresses data for places near a given location using a method which only uses one paid-for API call.
OS Names (free) is used to get an approximate location via eg. the street name, and then OS Places (paid-for) is used to get the nearby addresses.
The Names API allows for a free-text address search. If UPRN is known, then OpenUPRN can be used through the OS Features API instead.
"""

import requests

API_KEY = '7EfaXdK1HGuGs0j1dsp1vQoskVCQco6G'

# Pick a local type which is relevant to your search.
# Make sure the category is geographically small (eg, Named Road, Postcode, Bus Station)
# Avoid large categories (eg. City, Town, Suburban Area).
# https://docs.os.uk/os-downloads/addressing-and-location/os-open-names/os-open-names-technical-specification/code-lists/localtypevalue
LOCAL_TYPE = 'NAMED_ROAD'
PLACES_DATASET = 'DPA'
RADIUS = 1000  # in meters

NAMES_FIND_URI = 'https://api.os.uk/search/names/v1/find'
PLACES_RADIUS_URI = 'https://api.os.uk/search/places/v1/nearest'


def coords_from_names(local_type):
    """
    Get coordinates from OS Open Names API using a local type.
    """
    params = {
        'query': 'Fallowfield Close, Norwich',
        'fq': f'LOCAL_TYPE:{local_type}',
        'key': API_KEY,
    }

    names_response = requests.get(
        NAMES_FIND_URI,
        params=params,
        timeout=10
    ).json()

    first_result = names_response['results'][0]['GAZETTEER_ENTRY']

    x, y = first_result['GEOMETRY_X'], first_result['GEOMETRY_Y']

    return x, y


def get_places_nearby(x, y, radius, places_dataset):
    """
    Get places nearby using OS Open Places API.
    """
    params = {
        'point': f'{x},{y}',
        'radius': radius,
        'dataset': places_dataset,
        'key': API_KEY,
    }

    response = requests.get(
        PLACES_RADIUS_URI,
        params=params,
        timeout=10
    ).json()

    return response

def run():
    """
    Main function to run the script.
    """
    x, y = coords_from_names(LOCAL_TYPE)
    places_response = get_places_nearby(x, y, RADIUS, PLACES_DATASET)

    return places_response

run()
