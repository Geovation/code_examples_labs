"""
This script uses the OS Places API to finds all addresses with a specified postcode.
"""

import requests as r 


#Replace with your OS API key from the OS Data Hub
os_api_key = 'YOUR_OS_API_KEY'

#Replace with the postcode to search for
postcode_of_interest = 'EC1V 7EN'



def postcode_search(postcode, os_api_key):
    """
    This function find addresses from the OS Places API using a particular postcode.

    Args:
        poscode (str): The postcode to search for.
        os_api_key (str): Your OS API key.
    
    Returns:
        list: List of adrresses with the postcode of interest from OS Places API.
    """

    #OS Places API URL
    os_places_url = f'https://api.os.uk/search/places/v1/postcode'

    postcode_params = {
        'key': os_api_key,
        'postcode': postcode
    }

    response = r.get(os_places_url, params= postcode_params, timeout=10).json()

    results = response['results']

    #Extract the addresses as a list
    addresses = []
    for address in results:
        address = address['DPA']['ADDRESS']
        addresses.append(address)        

    print(f'Returning addresses for {postcode}')
    print(addresses)


    return addresses



postcode_search(postcode_of_interest, os_api_key)


