"""
This script uses the OS Places API to return addresses from a text search.
"""

import requests as r


# Replace with your OS API key from the OS Data Hub.
OS_API_KEY = 'YOUR_OS_API_KEY'

# Replace with the text query to search for.
QUERY = 'GEOVATION'

# Input the address dataset to search for, either DPA or LPI.
# See https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/datasets for more information.
DATASET = 'DPA'


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
