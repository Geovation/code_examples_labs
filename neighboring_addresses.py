'''
This example demonstrates how to use the OS Places API to find neighboring addresses
'''
import requests

# Replace with your API key
API_KEY = 'YOUR_API_KEY'

def get_nearby_addresses(address, radius):
    """
    Get nearby addresses within a specified radius from a given address.
    :param address: The address to search from.
    :param radius: The radius in meters to search for nearby addresses.
    :return: A list of nearby addresses.
    """
    query_uri = 'https://api.os.uk/search/places/v1/find'

    # Get the coordinates of the address
    query_response = requests.get(
        query_uri,
        params={'key': API_KEY, 'query': address},
        timeout=10
    ).json()
    first_result = query_response['results'][0]['DPA']
    x, y = first_result['X_COORDINATE'], first_result['Y_COORDINATE']

    # Radius search
    radius_uri = 'https://api.os.uk/search/places/v1/radius'
    radius_response = requests.get(
        radius_uri,
        params={
            'key': API_KEY,
            'point': f'{x},{y}',
            'radius': radius,
        },
        timeout=10
    ).json()
    return radius_response

def run():
    """
    Main function to run the function with example input.
    """
    # Replace with your address
    address = 'F4, Sutton Yard, 65 Goswell Rd., London EC1V 7EN'
    radius = 300  # in meters
    # Get the neighboring addresses
    radius_response = get_nearby_addresses(address, radius)
    print(radius_response)

run()
