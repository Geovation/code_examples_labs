"""
This script uses the OS Places API to return all addresses and address count within a specified bounding box.
"""

import requests as r 


# Replace with your OS API key from the OS Data Hub
OS_API_KEY = 'YOUR_OS_API_KEY'

# Replace with the bounding box coordinates to search for 
# Should be a pair of comma separated coordinates, to 2 decimal places or less, specifying the southwest and northeast corners of the bounding box
# Error message will be returned if the maximum size of the bounding box is exceeds 1km2
BBOX_COORDINATES = 'XMIN,YMIN,XMAX,YMAX'

# Input the address dataset to search for, which can be either DPA (Delivery Point Address) or LPI (Large Scale Addressing)
# See https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/datasets for more information
DATASET = 'DPA'


def bbox_search(bbox_coordinates):
    """
    This function finds addresses and calculates address count from the OS Places API within a specified bounding box.

    Args:
        bbox_coordinates (str): The bounding box coordinates to search for.
    
    Returns:
        list: List of addresses within the bounding box defined by the input coordinates from OS Places API.
        str: Number of addresses within the bounding box.
    """

    #OS Places API URL
    os_places_url = f'https://api.os.uk/search/places/v1/bbox'

    bbox_params = {
        'key': OS_API_KEY,
        'bbox': bbox_coordinates,
        'dataset' : DATASET                                                                                                                                                                                                                                                  
    }

    response = r.get(os_places_url, params= bbox_params, timeout=10).json()

    results = response['results']

    #Extract the addresses as a list
    addresses = []
    for address in results:
        address = address[DATASET]['ADDRESS']
        addresses.append(address)  

    #Calculate the number of addresses returned
    addresses_count = len(addresses)      

    print(f'Returning addresses within the bounding box [{bbox_coordinates}]')
    print(addresses)

    print(f'Number of addresses returned within the bounding box [{bbox_coordinates}]: {addresses_count}')


    return results



bbox_search(BBOX_COORDINATES)


