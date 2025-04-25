import requests
import re

os_api_key = 'YOUR API KEY HERE'
your_bounding_box = '-0.101472,51.522807,-0.096827,51.526016'

os_ngd_url = "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-1/items"
parameters = {"key": os_api_key, "bbox": your_bounding_box}

all_fetched_features = []
os_response = requests.get(url=os_ngd_url, params=parameters).json()


def is_valid_os_api_key(os_api_key):
    if re.match(r'^([a-zA-Z0-9]){32}$', os_api_key):
        return True
    else:
        print("Please enter a valid OS API Key")
        return False

is_valid_os_api_key(os_api_key)


while True:
    all_fetched_features.extend(os_response['features'])
    next_link = os_response['links'][-1] #This finds the last link in the array, is that the simplest?

    if next_link['rel'] == 'next':
        os_response = requests.get(next_link['href']).json()
    else:
        break

print(all_fetched_features)
