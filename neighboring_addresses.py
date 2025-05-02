'''
This example demonstrates how to use the OS Places API to find neighboring addresses
'''
import requests

# Replace with your API key
API_KEY = 'YOUR_API_KEY'
# Replace with your address
ADDRESS = 'F4, Sutton Yard, 65 Goswell Rd., London EC1V 7EN'
RADIUS = 300  # in meters

query_uri = 'https://api.os.uk/search/places/v1/find'

# Get the coordinates of the address
query_response = requests.get(
    query_uri,
    params={'key': API_KEY, 'query': ADDRESS},
    timeout=10
).json()
first_result = query_response['results'][0]['DPA']
x, y = first_result['X_COORDINATE'], first_result['Y_COORDINATE']

# 300m radius search
radius_uri = f'https://api.os.uk/search/places/v1/radius'
radius_response = requests.get(
    radius_uri,
    params={
        'key': API_KEY,
        'point': f'{x},{y}',
        'radius': RADIUS,
    },
    timeout=10
).json()

print(radius_response)
