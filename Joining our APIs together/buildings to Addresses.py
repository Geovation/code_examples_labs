import requests

YOUR_OS_API_KEY = 'YOUR API KEY HERE'

# Replace with the UPRN you want to search for. 100121341481 is Bradford on Avon library

# The collection and version of the NGD building data
BUILDINGS_COLLECTION = 'bld-fts-building-4'
bbox = "-0.10004, 51.524194,-0.099471, 51.524494"

NGD_FEATURES_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{BUILDINGS_COLLECTION}/items"


def match_buildings_to_addressses():
    uprns_to_fetch = []

    parameters = {
        "key": YOUR_OS_API_KEY,
        "bbox": bbox
    }

    os_response = requests.get(url=NGD_FEATURES_URL, params=parameters, timeout=10).json()

    for feature in os_response['features']:
        uprnreferences = feature['properties'].get('uprnreference')
        if uprnreferences:
            for values in uprnreferences:
                uprns_to_fetch.append(values['uprn'])

    os_places_url = "https://api.os.uk/search/places/v1/uprn?"

    parameters = {
        "key": YOUR_OS_API_KEY
    }

    full_addresses = []

    for uprn in uprns_to_fetch:
        parameters['uprn'] = uprn
        response = requests.get(url=os_places_url, params=parameters, timeout=10).json()
        print(requests.get(url=os_places_url, params=parameters, timeout=10).url)
        if 'results' in response and response['results']:
            for result in response['results']:
                full_addresses.append(result['DPA']['ADDRESS'])

    print(full_addresses)


match_buildings_to_addressses()