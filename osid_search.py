import requests
import re

os_api_key = 'YOUR_API_KEY_HERE'
collection_id = 'bld-fts-building-4'
other_parameters = {} # eg. {'crs': 'http://www.opengis.net/def/crs/EPSG/0/27700', 'filter': "buildinguse='Residential Accommodation'"}
os_ngd_url = f"https://api.os.uk/features/ngd/ofa/v1/collections/{collection_id}/items"
osids = [
    '2e36591e-0bd9-4268-99c2-0b653ac630d7',
    '6dca3202-39d9-4d8d-bf97-dd2bbf13550e',
    'eedf29cf-f1ff-4730-a882-6602922a0858',
    'a98fb1de-20de-44b4-96e5-2b0e7d15b78a',
    '7f01fa98-e3dc-4e3e-988e-7d3b8845e71f',
    'd5bce125-b5b4-45c0-8982-7b793e53e956',
    '17b545eb-e5aa-4ecf-9efe-8b40aacf4c16',
    'c69b6ec4-ada0-45e0-b22a-cc01a1efa2f7',
    '278af03f-a590-4723-af54-92e16726f1e7',
    '6bc5230a-b008-44ca-ab8f-6bee4040f38e',
    '9aa4d5ab-bbea-46b2-a5df-f4a30434c685',
    '2ed5d76f-b31d-47c2-9f1c-0555b659ce35'
]

def is_valid_os_api_key(os_api_key):
    if re.match(r'^([a-zA-Z0-9]){32}$', os_api_key):
        return True
    else:
        print("Please enter a valid OS API Key")
        return False

is_valid_os_api_key(os_api_key)

def osids_to_filter_string(osids):
    """
    Convert a list of OSIDs to a filter string for the API request.
    """
    filter_units = [f"(osid='{id}')" for id in osids]
    filter_string = 'or'.join(filter_units)
    return filter_string

filter_string = osids_to_filter_string(osids)

# Merge osid filter with other filters if present
existing_filter = other_parameters.pop('filter', None)
if existing_filter:
    filter_string = f"({filter_string})and({existing_filter})"

parameters = {
    "key": os_api_key,
    "filter": filter_string,
    **other_parameters
}

print(f'requesting {os_ngd_url} with parameters {parameters}')
os_response = requests.get(url=os_ngd_url, params=parameters).json()

print(os_response)