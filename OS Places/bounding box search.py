"""
This script uses the OS Places API to return all addresses and address count within a specified
bounding box.
"""

import requests as r


# Replace with your OS API key from the OS Data Hub.
OS_API_KEY = 'YOUR_OS_API_KEY'

# Replace with the coordinates (2dp or less) of the southwest and northeast corners of the bounding
# box to search for.
# An error message will be returned if the maximum size of the bounding box exceeds 1km2.
BBOX_COORDINATES = '437256.6, 115481.3, 437376.4, 115601.7'

# Input the address dataset to search for, either DPA (Delivery Point Address) or LPI
# (Large Scale Addressing).
# See https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/datasets for more information.
DATASET = 'DPA'


def bbox_search(bbox_coordinates):
    """
    This function finds addresses from the OS Places API and calculates the address count within a
    specified bounding box.

    Args:
        bbox_coordinates (str): The bounding box coordinates to search for.
    
    Returns:
        list: List of addresses within the bounding box defined from OS Places API.
        str: Number of addresses within the bounding box.
    """

    # OS Places API URL.
    os_places_url = 'https://api.os.uk/search/places/v1/bbox'

    bbox_params = {
        'key': OS_API_KEY,
        'bbox': bbox_coordinates,
        'dataset' : DATASET,
        'srs': 'EPSG:27700'                                                                                                                                                                                                                                    
    }

    response = r.get(os_places_url, params= bbox_params, timeout=10).json()

    results = response['results']

    # Extract the addresses as a list.
    addresses = []
    for address in results:
        address = address[DATASET]['ADDRESS']
        addresses.append(address)

    # Calculate the number of addresses returned.
    # Note: Maximum count will be 100 even if the actual number of addresses within the search area
    # is greater, as the API returns a maximum of 100 addresses.
    addresses_count = len(addresses)

    print(f'Returning addresses within the bounding box [{bbox_coordinates}]:')
    print(addresses)

    print(f'Number of addresses returned within the bounding box: {addresses_count}')


    return addresses



bbox_search(BBOX_COORDINATES)
