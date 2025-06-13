import requests

YOUR_OS_API_KEY = 'YOUR_OS_API_KEY'

# Replace with the UPRN you want to search for. 100121341481 is Bradford on Avon library

# The collection and version of the NGD building data
BUILDINGS_COLLECTION = 'bld-fts-building-4'
SITES_COLLECTION = 'lus-fts-site-2'
bbox = "-0.10004, 51.524194,-0.099471, 51.524494"

NGD_BUILDINGS_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{BUILDINGS_COLLECTION}/items"

NGD_sites_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{SITES_COLLECTION}/items"


def match_buildings_to_addressses():
    site_osid = []

    parameters = {
        "key": YOUR_OS_API_KEY,
        "bbox": bbox
    }

    os_response = requests.get(url=NGD_BUILDINGS_URL, params=parameters, timeout=10).json()

    for feature in os_response['features']:
        if feature['properties']['primarysiteid'] is not None:
            site_osid.append(feature['properties']['primarysiteid'])



    filter_units = []
    for osid in site_osid:
        filter_units.append(f"(osid='{osid}')")

    filter_string = 'or'.join(filter_units)

    parameters = {
        "key": YOUR_OS_API_KEY,
        "filter": filter_string
    }

    os_response = requests.get(url=NGD_sites_URL, params=parameters, timeout=10).json()

    print(os_response)


match_buildings_to_addressses()

