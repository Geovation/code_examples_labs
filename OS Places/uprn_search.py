"""
This script uses the OS Places API to return addresses with a specific UPRN.
"""

import requests as r


# Replace with your OS API key from the OS Data Hub.
OS_API_KEY = 'YOUR_OS_API_KEY'

# Replace with the UPRN to search for.
UPRN_OF_INTEREST = '10094608166'

# Input the address dataset to search for, either DPA or LPI.
# See https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/datasets for more information.
DATASET = 'DPA'


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
