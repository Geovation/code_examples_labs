"""
This script provides an example for retrieving features from the National Geographic Database
(NGD) API using pagination to retrieve data within a specified bounding box.
"""

import requests

# Use your OS API key from the OS Data Hub, a string of 32 characters
# Note: The API key should be kept secret and not shared publicly
YOUR_OS_API_KEY = 'YOUR_OS_API_KEY'

# Replace with your bounding box: 'min_longitude,min_latitude,max_longitude,max_latitude'
YOUR_BOUNDING_BOX = '-0.101472,51.522807,-0.096827,51.526016'

# Set the maximum number of results to 0 for unlimited pagination
MAX_RESULTS = 500

# The NGD collection name and version e.g. "bld-fts-building-4"
NGD_COLLECTION = "bld-fts-building-4"

OS_NGD_URL = f"https://api.os.uk/features/ngd/ofa/v1/collections/{NGD_COLLECTION}/items"


def run_paginated_requests():
    """
    This function uses the supplied parameters to make paginated requests to the OS NGD API.
    """

    # The request limit is set to 100 or MAX_RESULTS if that is less than 100
    request_limit = min(100, MAX_RESULTS) if MAX_RESULTS != 0 else 100

    # The 'limit' parameter specifies the maximum number of features to return in a single response
    # The 'offset' parameter is for pagination, and is the starting point for the set of results
    request_parameters = {"key": YOUR_OS_API_KEY,
                          "bbox": YOUR_BOUNDING_BOX, "limit": request_limit, "offset": None}

    all_fetched_features = []

    next_link = None

    # Always run once while next_link is None then run till no next_link is found
    while next_link is None or next_link is True:

        next_link = False

        # Fetch the features from the OS NGD API
        os_response = requests.get(
            url=OS_NGD_URL, params=request_parameters, timeout=10).json()

        # Check if the response contains any features
        if 'features' not in os_response or len(os_response['features']) == 0:
            print("No features found in the response.")
            break

        # Add the fetched features to the list
        all_fetched_features.extend(os_response['features'])

        # Update the offset based upon the fetched features
        request_parameters['offset'] = len(all_fetched_features)

        # Set next link to True if there is a next link in the links section of the response
        next_link = any(
            link['rel'] == 'next' for link in os_response.get('links', []))

        # If the maximum number of results is set, check if we have reached it
        if MAX_RESULTS != 0 and len(all_fetched_features) >= MAX_RESULTS:
            print(f"Reached the maximum number of results: {MAX_RESULTS}")
            break

    print(all_fetched_features)


run_paginated_requests()
