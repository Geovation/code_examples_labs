"""This script retrieves building information from the OS NGD API using a list of OSIDs."""

import requests

OS_API_KEY = 'YOUR_OS_API_KEY'

def osid_search(collection_id, osids):
    """
    This function retrieves building information from the OS NGD API using a list of OSIDs.
    :param collection_id: The ID of the collection to search in.
    :param osids: A list of OSIDs to search for.
    :return: A JSON response containing the building information.
    """

    os_ngd_url = f"https://api.os.uk/features/ngd/ofa/v1/collections/{collection_id}/items"

    filter_units = []
    for osid in osids:
        filter_units.append(f"(osid='{osid}')")

    filter_string = 'or'.join(filter_units)

    parameters = {
        "key": OS_API_KEY,
        "filter": filter_string
    }

    print(f'requesting {os_ngd_url} with parameters {parameters}')
    os_response = requests.get(url=os_ngd_url, params=parameters, timeout=10).json()

    return os_response

def run():
    """
    Main function to retrieve the NGD Building data for some example OSIDs.
    """
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
    collection_id = 'bld-fts-building-4'
    example = osid_search(collection_id, osids)
    print(example)

run()
