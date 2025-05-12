"""
Retrieve main building from a given site name using the OS NGD Features API
Sites are a feature type within the NGD Land Use features
Buildings are a feature type within the NGD Building features
"""

import requests

# Use your OS API key from the OS Data Hub, a string of 32 characters
# Note: The API key should be kept secret and not shared publicly
YOUR_OS_API_KEY = 'YOUR_OS_API_KEY'

# The collection and version of the NGD land use data
SITE_FEATURES = 'lus-fts-site-2'

# The collection and version of the NGD building data
BUILDINGS_COLLECTION = 'bld-fts-building-4'

SITE_FEATURES_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{SITE_FEATURES}/items"

BUILDING_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{BUILDINGS_COLLECTION}/items/"

SITE_NAME = 'University of Exeter'


def get_site_from_site_name():
    """
    Gets a site from the OS NGD Features API using the name of the site.
    This assumes the first match is the correct one - this may not be the case
    so be careful with this.
    """

    site_name_filter = f"name1_text='{SITE_NAME}'"

    site_parameters = {
        "key": YOUR_OS_API_KEY,
        "filter": site_name_filter
    }

    site_response = requests.get(
        url=SITE_FEATURES_URL, params=site_parameters, timeout=10).json()

    if site_response['features']:
        return site_response['features'][0]

    print(f"No site found for name {SITE_NAME}")
    return None


def get_building_from_osid(osid):
    """
    Get the NGD building data from a given osid (a unique identifier for a building).
    """

    building_parameters = {
        "key": YOUR_OS_API_KEY
    }

    buildings_response = requests.get(
        url=f"{BUILDING_URL}{osid}", params=building_parameters, timeout=10).json()

    return buildings_response


def run():
    """
    Main function to retrieve the NGD building data for a given site name
    """

    site = get_site_from_site_name()
    if site and 'properties' in site and 'mainbuildingid' in site['properties']:
        building_osid = site['properties']['mainbuildingid']
        print(f"Main building OSID for {SITE_NAME} is {building_osid}")
        building_data = get_building_from_osid(building_osid)
        print(building_data)
    else:
        print(f"No main building data found for site name {SITE_NAME}")


run()
