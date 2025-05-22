"""
This script uses the OS Places API to return addresses within a defined polygon search area.
"""

import requests as r


# Replace with your OS API key from the OS Data Hub.
OS_API_KEY = 'YOUR_OS_API_KEY'

# Replace with GeoJSON geometry of the search polygon.
GEOMETRY = {
  "type": "Feature",
  "geometry": {"type": "Polygon",
            "coordinates": [
                [
                    [ 437264.6,	115475.8 ],
                    [ 437238.7, 115593.2 ],
                    [ 437309.1, 115618.6 ],
                    [ 437384.0, 115590.7 ],
                    [ 437264.6,	115475.8 ]
                ]
            ]
        }
}

# Input the address dataset to search for, either DPA or LPI.
# See https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/datasets for more information.
DATASET = 'DPA'


def polygon_search(geometry):
    """
    This function returns addresses from the OS Places API that are within a specified polygon area.

    Args:
        geometry (geojson): The polygon search area of interest.
    
    Returns:
        list: List of adrresses within the defined polygon search area from OS Places API.
    """

    # OS Places API URL.
    os_places_url = 'https://api.os.uk/search/places/v1/polygon'

    header = {
        'Content-Type': 'application/json'
    }

    polygon_params = {
        'key': OS_API_KEY,
        'dataset' : DATASET,
        'srs': 'EPSG:27700'                                                                                                                                                                                                                                                  
    }

    response = r.post(
        os_places_url, headers=header, json=geometry, params= polygon_params, timeout=10
        ).json()

    results = response['results']

    # Extract the addresses as a list.
    addresses = []
    for address in results:
        address = address[DATASET]['ADDRESS']
        addresses.append(address)


    print('Returning addresses within the polygon search area:')
    print(addresses)


    return addresses



polygon_search(GEOMETRY)
