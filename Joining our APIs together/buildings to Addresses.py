import requests

YOUR_OS_API_KEY = 'MGLREA5yR0hYbjXjcGn0Y4i3VODTPLIK'

# Replace with the UPRN you want to search for. 100121341481 is Bradford on Avon library

# The collection and version of the NGD building data
BUILDINGS_COLLECTION = 'bld-fts-building-4'
bbox = "-0.10004, 51.524194,-0.099471, 51.524494"

NGD_FEATURES_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{BUILDINGS_COLLECTION}/items"

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

os_places_url = "https://api.os.uk/search/places/v1/UPRN?"

parameters = {
    "key": YOUR_OS_API_KEY,
}

full_addresses = []

for uprn in

print(uprns_to_fetch)
