"""
Retrieve NGD Building data from a given UPRN using the NGD Features API and OS Features API.
"""

import requests

# Use your OS API key from the OS Data Hub, a string of 32 characters
# Note: The API key should be kept secret and not shared publicly
YOUR_OS_API_KEY = ''

# Replace with the UPRN you want to search for. 100121341481 is Bradford on Avon library
UPRN_TO_SEARCH = 100121341481

# The collection and version of the NGD building data
BUILDINGS_COLLECTION = 'bld-fts-building-4'

OS_FEATURES_URL = "https://api.os.uk/features/v1/wfs"
NGD_FEATURES_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{BUILDINGS_COLLECTION}/items"


def get_uprn_coordinates():
    """
    Get the coordinates of a given UPRN using OpenUPRN within the OS Features API (free).
    """

    # The XML filter is a string that specifies the UPRN to search for
    uprn_filter = f"<ogc:Filter><ogc:PropertyIsEqualTo><ogc:PropertyName>UPRN</ogc:PropertyName><ogc:Literal>{UPRN_TO_SEARCH}</ogc:Literal></ogc:PropertyIsEqualTo></ogc:Filter>"

    uprn_request_parameters = {
        'request': 'GetFeature',
        'service': 'WFS',
        'version': '2.0.0',
        'typeNames': 'OpenUPRN_Address',
        'outputFormat': 'GEOJSON',
        'filter': requests.utils.quote(uprn_filter)
    }

    # Make the request to the OpenUPRN API
    response = requests.get(url=OS_FEATURES_URL, headers={'key': YOUR_OS_API_KEY},
                            params=uprn_request_parameters, timeout=10)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    coordinates = None

    data = response.json()
    if data['features']:
        coordinates = data['features'][0]['geometry']['coordinates']
    else:
        print(f"No features found for UPRN {UPRN_TO_SEARCH}")

    return coordinates


def get_ngd_building_from_point(coordinates):
    """
    Get the NGD building data from a given set of coordinates using the OS NGD Features API
    and filter by the UPRN.
    """

    point_filter = f"INTERSECTS(geometry, POINT({coordinates[0]} {coordinates[1]}))"

    building_request_parameters = {
        'filter': point_filter,
    }

    response = requests.get(url=NGD_FEATURES_URL, headers={'key': YOUR_OS_API_KEY},
                            params=building_request_parameters, timeout=10)

    building = None

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    data = response.json()
    if data['features']:
        # Check through to see if the uprnreference matches e.g. 'uprnreference': [{'uprn': 1}
        for feature in data['features']:
            if 'uprnreference' in feature['properties']:
                uprn_references = feature['properties']['uprnreference']
                for uprn_reference in uprn_references:
                    if uprn_reference['uprn'] == UPRN_TO_SEARCH:
                        building = feature
                        break
    else:
        print(f"No building found for coordinates {coordinates}")

    return building


def run():
    """
    Main function to retrieve the NGD building data from a given UPRN.
    """

    coordinates = get_uprn_coordinates()
    if coordinates:
        print(f"Coordinates for UPRN {UPRN_TO_SEARCH}: {coordinates}")
        building = get_ngd_building_from_point(coordinates)
        if building:
            print(f"Building data for UPRN {UPRN_TO_SEARCH}: {building}")
        else:
            print(f"No building data found for UPRN {UPRN_TO_SEARCH}")
    else:
        print(f"No coordinates found for UPRN {UPRN_TO_SEARCH}")


run()
