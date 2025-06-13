"""
This script illustrates how to use the OS Places API to search for addresses using different
methods.
"""

import requests as r


# CONSTANTS ##

# Replace with your OS API key from the OS Data Hub.
OS_API_KEY = 'YOUR_OS_API_KEY'

# Input the address dataset to search for, either DPA or LPI.
# See https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/datasets for more information.
DATASET = 'DPA'

# METHOD 1: FREE TEXT SEARCH

# Replace with the text query to search for.
QUERY = 'GEOVATION'


def query_search(text):
    """
    This function returns addresses from a text search from the OS Places API.

    Args:
        text (str): The search text query.

    Returns:
        list: List of addresses with the text query from OS Places API.
    """

    # OS Places API URL.
    os_places_url = 'https://api.os.uk/search/places/v1/find'

    text_params = {
        'key': OS_API_KEY,
        'query': text,
        'dataset' : DATASET  
    }

    response = r.get(os_places_url, params= text_params, timeout=10).json()

    results = response['results']

    # Return addresses with a possible match with the query.
    possible_matches = [result[DATASET]['ADDRESS'] for result in results]
    print(f'Returning possible addresses with query {text}:')
    print(possible_matches)

    return possible_matches


query_search(QUERY)

# METHOD 2: POSTCODE SEARCH

# Replace with the postcode to search for.
POSTCODE_OF_INTEREST =  'SO16 0AS'


def postcode_search(postcode):
    """
    This function finds addresses from the OS Places API using a particular postcode.

    Args:
        postcode (str): The postcode to search for.
    
    Returns:
        list: List of addresses with the postcode of interest from OS Places API.
    """

    # OS Places API URL.
    os_places_url = 'https://api.os.uk/search/places/v1/postcode'

    postcode_params = {
        'key': OS_API_KEY,
        'postcode': postcode
    }

    response = r.get(os_places_url, params= postcode_params, timeout=10).json()

    results = response['results']

    # Extract the addresses as a list.
    # Note: DPA (Delivery Point Address) are postal addresses, the most appropriate address database
    # for a postcode search for delivery addresses.
    addresses = []
    for address in results:
        address = address['DPA']['ADDRESS']
        addresses.append(address)

    print(f'Returning addresses for {postcode}:')
    # print each address on a new line

    print('\n'.join(addresses))

    return addresses


postcode_search(POSTCODE_OF_INTEREST)


# Replace with the UPRN to search for.
UPRN_OF_INTEREST = '10094608166'


def uprn_search(uprn):
    """
    This function returns the address information from the OS Places API using a particular UPRN.

    Args:
        uprn (str): The UPRN to search for.

    Returns:
       json: Address information with the specified UPRN from OS Places API.
    """

    # OS Places API URL.
    os_places_url = 'https://api.os.uk/search/places/v1/uprn'

    uprn_params = {
        'key': OS_API_KEY,
        'uprn': uprn,
        'dataset' : DATASET  
    }

    response = r.get(os_places_url, params= uprn_params, timeout=10).json()

    results = response['results']

    print(f'Returning address entry for {uprn}:')
    print(results)

    return results


uprn_search(UPRN_OF_INTEREST)

# METHOD 4: BOUNDING BOX SEARCH

# Replace with the coordinates (2dp or less) of the southwest and northeast corners of the bounding
# box to search for.
# An error message will be returned if the maximum size of the bounding box exceeds 1km2.
BBOX_COORDINATES = '437256.6, 115481.3, 437376.4, 115601.7'


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

# METHOD 5: RADIUS SEARCH

# Replace with the point coordinate (2dp or less) of the centre of the search circle.
RADIUS_COORDINATES = '437297.4, 115541.6'

# Replace with the radius of the search circle.
RADIUS = '100'


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

# METHOD 6: POLYGON SEARCH

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
