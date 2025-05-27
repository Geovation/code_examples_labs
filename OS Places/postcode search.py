"""
This script uses the OS Places API to find all addresses with a specified postcode.
"""

import requests as r


# Replace with your OS API key from the OS Data Hub.
OS_API_KEY = 'YOUR_OS_API_KEY'

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
    print('\n'.join(addresses))     #print each address on a new line


    return addresses



postcode_search(POSTCODE_OF_INTEREST)
