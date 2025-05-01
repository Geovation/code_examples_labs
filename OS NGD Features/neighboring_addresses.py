'''
This example demonstrates how to use the OS Places API to find neighboring addresses
'''
import requests

# Replace with your API key
API_KEY = 'YOUR_API_KEY'
# Replace with your address
ADDRESS = 'F4, Sutton Yard, 65 Goswell Rd., London EC1V 7EN'

QUERY_URI = 'https://api.os.uk/search/places/v1/find?query=' + ADDRESS
query_response = requests.get(
    QUERY_URI, params={'key': API_KEY}, timeout=10).json()
first_result = query_response['results'][0]['DPA']

x, y = first_result['X_COORDINATE'], first_result['Y_COORDINATE']
# 300m radius search
RADIUS_URI = f'https://api.os.uk/search/places/v1/radius?point={x},{y}&radius=300'

radius_response = requests.get(RADIUS_URI, params={'key': API_KEY}, timeout=10).json()
print(radius_response)
