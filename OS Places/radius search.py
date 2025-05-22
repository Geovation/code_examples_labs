"""
This script uses the OS Places API to return addresses within a defined radius search area.
"""

import requests as r


# Replace with your OS API key from the OS Data Hub.
OS_API_KEY = 'YOUR_OS_API_KEY'

# Replace with the point coordinate (2dp or less) of the centre of the search circle.
RADIUS_COORDINATES = '437297.4, 115541.6'

# Replace with the radius of the search circle.
RADIUS = '100'

# Input the address dataset to search for, either DPA or LPI.
# See https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/datasets for more information.
DATASET = 'DPA'


def radius_search(radius_coordinates):
    """
    This function returns addresses from the OS Places API that are within a defined search radius
    from a given point.

    Args:
        radius_coordinates (str): The point coordinates of the centre of the search circle.
    
    Returns:
        list: List of addresses within the search circle from OS Places API.
    """

    # OS Places API URL.
    os_places_url = 'https://api.os.uk/search/places/v1/radius'

    radius_params = {
        'key': OS_API_KEY,
        'point': radius_coordinates,
        'radius': RADIUS,
        'dataset' : DATASET,
        'srs': 'EPSG:27700'                                                                                                                                                                                                                                                  
    }

    response = r.get(os_places_url, params= radius_params, timeout=10).json()

    results = response['results']

    # Extract the addresses as a list.
    addresses = [address[DATASET]['ADDRESS'] for address in results]

    print(f'Returning addresses within the circle search area from point {RADIUS_COORDINATES}:')
    print(addresses)


    return addresses



radius_search(RADIUS_COORDINATES)
