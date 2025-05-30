import requests

YOUR_OS_API_KEY = '00kut4MHNU5pXqP2zQDJnx5ANcrgpBNK'

# Replace with the UPRN you want to search for. 100121341481 is Bradford on Avon library

# The collection and version of the NGD building data
BUILDINGS_COLLECTION = 'bld-fts-building-4'
bbox = "-0.10004, 51.524194,-0.099471, 51.524494"

NGD_FEATURES_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{BUILDINGS_COLLECTION}/items"


def match_buildings_to_addressses():
    site_osid = []

    parameters = {
        "key": YOUR_OS_API_KEY,
        "bbox": bbox
    }

    os_response = requests.get(url=NGD_FEATURES_URL, params=parameters, timeout=10).json()

    for feature in os_response['features']:
       site_osid.append(feature['properties']['primarysiteid'])




match_buildings_to_addressses()

