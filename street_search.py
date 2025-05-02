"""This script demostrates an OS-data-based approach to find all the addresses on the same road as a given address."""

import requests
from shapely import MultiLineString, LineString, set_precision, to_geojson

# Setup: Replace with your API key, and set your own address and buffer distance
API_KEY = 'eEAntN52ODqwXAKY30dqXUibMI8EDzab'
ADDRESS = 'F4, Sutton Yard, 65 Goswell Rd., London EC1V 7EN'
BUFFER_DISTANCE = 20  # in meters
DATASET = 'LPI'  # Dataset for the final search: DPA or LPI
# Set to True if you want to filter final results for those matching the USRN.
# Only possible if DATASET is LPI.
FILTER_FOR_USRN = True

# 1: Retreive the USRN of the address
query_uri = 'https://api.os.uk/search/places/v1/find?query=' + ADDRESS
# Get the coordinates of the address
query_response = requests.get(
    query_uri,
    params={'dataset': 'LPI', 'key': API_KEY},
    timeout=10
).json()
first_result = query_response['results'][0]['LPI']
usrn = first_result['USRN']

# 2: Get the geometry of the USRN
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
params = {
    'key': API_KEY,
    'request': 'GetFeature',
    'service': 'WFS',
    'version': '2.0.0',
    'outputFormat': 'geojson',
    'typeNames': 'OpenUSRN_USRN',
    'srsName': 'EPSG:27700',
    'filter': usrn_filter
}
features_api_uri = 'https://api.os.uk/features/v1/wfs'
features_response = requests.get(
    features_api_uri,
    params=params,
    timeout=10
).json()
geometry = features_response['features'][0]['geometry']

# 3: Buffer the geometry
ShapeType = geometry['type']
Constructor = MultiLineString if ShapeType == 'MultiLineString' else LineString
shape = Constructor(geometry['coordinates'])
buffered_shape = shape.buffer(BUFFER_DISTANCE, resolution=4)
buffered_shape = set_precision(buffered_shape, 1)

# 4: Search for addresses within the street
geojson = to_geojson(buffered_shape)
polygon_search_uri = 'https://api.os.uk/search/places/v1/polygon'
headers = {'Content-Type': 'application/json'}

places_response = requests.post(
    polygon_search_uri,
    params={'key': API_KEY, 'dataset': DATASET},
    data=geojson,
    headers=headers,
    timeout=10
).json()
results = places_response['results']

# 5: Filter results for USRN if required
if FILTER_FOR_USRN and DATASET == 'LPI':
    results = [r for r in results if r['LPI']['USRN'] == usrn]
