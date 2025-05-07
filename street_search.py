"""This script demostrates an OS-data-based approach to find all the addresses on the same road as a given address."""

import requests
from shapely import MultiLineString, LineString, to_geojson

# Setup: Replace with your API key, and set your own address and buffer distance
API_KEY = 'YOUR_OS_API_KEY'

PLACES_FIND_ENDPOINT = 'https://api.os.uk/search/places/v1/find'
FEATURES_ENDPOINT = 'https://api.os.uk/features/v1/wfs'
PLACES_POLYGON_ENDPOINT = 'https://api.os.uk/search/places/v1/polygon'

def retrieve_address_usrn(address):
    """Retrieve the USRN of the address using the OS Places API."""
    query_response = requests.get(
        PLACES_FIND_ENDPOINT,
        params={
            'query': address,
            'dataset': 'LPI',
            'key': API_KEY
        },
        timeout=10
    ).json()
    first_result = query_response['results'][0]['LPI']
    usrn = first_result['USRN']
    return usrn


def get_ogc_filter(usrn):
    """Get the geometry of the USRN using an OGC filter."""
    usrn_filter_formatted = f"""
    <ogc:Filter>
        <ogc:PropertyIsEqualTo>
            <ogc:PropertyName>
                USRN
            </ogc:PropertyName>
            <ogc:Literal>
                {usrn}
            </ogc:Literal>
        </ogc:PropertyIsEqualTo>
    </ogc:Filter>"""
    usrn_filter = usrn_filter_formatted.replace(' ', '').replace('\n', '')
    features_response = requests.get(
        FEATURES_ENDPOINT,
        params={
            'request': 'GetFeature',
            'service': 'WFS',
            'version': '2.0.0',
            'outputFormat': 'geojson',
            'typeNames': 'OpenUSRN_USRN',
            'srsName': 'EPSG:27700',
            'filter': usrn_filter,
            'key': API_KEY
        },
        timeout=10
    ).json()
    geometry = features_response['features'][0]['geometry']
    return geometry


def buffer_geometry(geometry, buffer_distance):
    """Buffer the geometry by the specified distance."""
    ShapeType = geometry['type']
    Constructor = MultiLineString if ShapeType == 'MultiLineString' else LineString
    shape = Constructor(geometry['coordinates'])
    buffered_shape = shape.buffer(buffer_distance, resolution=4)
    return buffered_shape

def address_search(shape, dataset):
    """Search for addresses within the buffered geometry."""
    geojson = to_geojson(shape)
    polygon_search_uri = 'https://api.os.uk/search/places/v1/polygon'
    headers = {'Content-Type': 'application/json'}
    places_response = requests.post(
        polygon_search_uri,
        params={
            'dataset': dataset,
            'key': API_KEY
        },
        data=geojson,
        headers=headers,
        timeout=10
    ).json()
    results = places_response['results']
    return results

def filter_results(results, usrn):
    """Filter results to only include those with the specified USRN."""
    filtered_results = []
    for r in results:
        if r['LPI']['USRN'] == usrn:
            filtered_results.append(r)
    return filtered_results

def run():
    """Main function to run the address search."""
    address = 'F4, Sutton Yard, 65 Goswell Rd., London EC1V 7EN'
    buffer_distance = 20  # in meters
    dataset = 'LPI'  # Dataset for the final search: DPA or LPI
    # Set to True if you want to filter final results for those matching the USRN.
    # Only possible if 'dataset' is LPI.
    filter_for_usrn = True

    # 1: Retrieve the USRN of the address
    usrn = retrieve_address_usrn(address)
    # 2: Get the geometry of the USRN
    geometry = get_ogc_filter(usrn)
    # 3: Buffer the geometry
    buffered_shape = buffer_geometry(geometry, buffer_distance)
    # 4: Search for addresses within the street
    results = address_search(buffered_shape, dataset)
    # 5: Filter results for USRN if required
    if filter_for_usrn and dataset == 'LPI':
        results = filter_results(results, usrn)
    print(results)
    return results


run()
