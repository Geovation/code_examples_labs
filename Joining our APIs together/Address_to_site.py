"""
Retrieve NGD Sites data from a given address using the NGD Features API and OS Places API.
"""

import requests

# Use your OS API key from the OS Data Hub, a string of 32 characters
# Note: The API key should be kept secret and not shared publicly
YOUR_OS_API_KEY = 'YOUR_OS_API_KEY'

# The collection and version of the NGD site data
sites_collection = 'lus-fts-site-2'
# Options include find, postcode and UPRN
places_path = 'find'
OS_PLACES_URL = f"https://api.os.uk/search/places/v1/{places_path}"
NGD_FEATURES_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{sites_collection}/items"


def address_to_cords(address):

    address_request_paremeters = {'output_srs': 'EPSG:4326',
                                  'query':address ,
                                  'dataset': 'DPA'}

    response = requests.get(url=OS_PLACES_URL, params=address_request_paremeters, headers={'key': YOUR_OS_API_KEY},)
    wgs84_cords = response.json()["results"][0]["DPA"]["LNG"], response.json()["results"][0]["DPA"]["LAT"]
    uprn = response.json()["results"][0]["DPA"]['UPRN']

    return wgs84_cords, uprn


def get_ngd_site_from_point(coordinates, uprn_to_match):
    """
    Get the NGD site data from a given set of coordinates using the OS NGD Features API
    and filter by the UPRN.
    """

    point_filter = f"INTERSECTS(geometry, POINT({coordinates[0]} {coordinates[1]}))"

    site_request_params = {
        'filter': point_filter,
    }

    response = requests.get(url=NGD_FEATURES_URL, headers={'key': YOUR_OS_API_KEY},
                            params=site_request_params, timeout=10)
    print(response.url)

    site = None

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()
    print(data)

    if data['features']:
        # Check through to see if the uprnreference matches e.g. 'uprnreference': [{'uprn': 1}
        for feature in data['features']:
            print(feature['properties'] )
            if 'sitetoaddressreference' in feature['properties']:
                uprn_references = feature['properties']['sitetoaddressreference']
                for uprn_reference in uprn_references:
                    if uprn_reference['uprn'] == int(uprn_to_match):
                        site = feature
                        break
    else:
        print(f"No site found for coordinates {coordinates}")

    return site


def run():
    """
    Main function to retrieve the NGD site data from a given address.
    """
    address_as_string = 'Rose and Crown langport'

    coordinates, uprn_to_search = address_to_cords(address_as_string)
    if coordinates:
        print(f"Coordinates for UPRN {uprn_to_search}: {coordinates}")
        site = get_ngd_site_from_point(coordinates, uprn_to_search)
        if site:
            print(f"site data for UPRN {uprn_to_search}: {site}")
        else:
            print(f"No site data found for UPRN {uprn_to_search}")
    else:
        print(f"No coordinates found for UPRN {uprn_to_search}")


run()
