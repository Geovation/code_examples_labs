"""
Match unstructured or manually typed addresses to those held in AddressBase by searching OS Places
Customise the script to suit your needs by using your own input data and address scoring criteria
This script uses the OS Places API to match addresses from a CSV file against the OS Places dataset.
"""

import csv
import time
import requests

# Use your OS API key from the OS Data Hub, a string of 32 characters
# Note: The API key should be kept secret and not shared publicly
YOUR_OS_API_KEY = 'YOUR_OS_API_KEY'

# Define the path to the CSV file containing the sample addresses
SAMPLE_DATA_FILE = "./Data/sample_addresses.csv"

# Define the path to the output CSV file where matched addresses will be saved
OUTPUT_FILE = "./Data/matched_addresses.csv"

# Define the fields in your data (CSV file) that represent the address
# For the best matching, these should be in the correct address order
ADDRESS_SEARCH_FIELDS = [
    "Name", "Address 1", "Address 2", "Address 3", "Postcode"
]

# Define the fields to be added to the CSV file from OS Places
# For example you could just add UPRN if you want a unique identifier but want
# to keep the original address data (e.g. these could have been typed by users)
# See https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/datasets
ADDRESS_MATCH_FIELDS = [
    "UPRN"
]

# The match score will assess the quality of the match with AddressBase
# 1.0 is a perfect match, 0.8-0.9 is a good match, 0.7 is a partial match
# You could start with a higher score and assess the results
REQUIRED_MATCH_SCORE = 0.7

# For code lists see https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/code-lists
# e.g. for country codes E = England, N = Northern Ireland, S = Scotland, W = Wales
CODES = "COUNTRY_CODE:E"

# Customise the returned address dataset to your needs . This is either LPI or DPA
# See https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/datasets
DATASET = "LPI"

PLACES_API_URL = "https://api.os.uk/search/places/v1/find"


def read_address_csv():
    """
    Read the CSV file and return a list of dictionaries of the specified address fields.
    Each dictionary represents a row in the CSV file.
    """

    with open(SAMPLE_DATA_FILE, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        addresses = []
        for row in reader:
            address = {field: row[field] for field in ADDRESS_SEARCH_FIELDS}
            addresses.append(address)
    return addresses


def get_matching_address(address):
    """
    Call the OS Places API to retrieve the first match and a score for the given address.
    """

    # Construct the parameters for the API request
    request_params = {
        "query": address,
        "dataset": DATASET,
        "maxresults": 1,
        "minmatch": REQUIRED_MATCH_SCORE,
        "fq": CODES,
    }

    # Make the API request
    response = requests.get(PLACES_API_URL, headers={
                            'key': YOUR_OS_API_KEY}, params=request_params, timeout=30)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0][DATASET]
    return None


def run():
    """
    Function to execute the address matching process.
    """

    # Read the addresses from the CSV file
    addresses = read_address_csv()

    matches = 0
    # For each address call the OS Places API to retrieve the first match and a score
    for address in addresses:
        # Join the address fields into a single string
        address_str = ", ".join([address[field]
                                 for field in ADDRESS_SEARCH_FIELDS if address[field]])

        # Remove any quotes from the address string (if a field entry contained a comma)
        address_str = address_str.replace('"', '')
        # Remove any leading or trailing whitespace
        address_str = address_str.strip()

        print(f"Searching for: {address_str}")
        # Call the OS Places API to get the matching address
        matching_address = get_matching_address(address_str)
        if matching_address:
            # Add all the ADDRESS_MATCH_FIELDS to the address
            for field in ADDRESS_MATCH_FIELDS:
                if field in matching_address:
                    address[field] = matching_address[field]
                    matches += 1

        # There is a rate limit of 600 requests per minute
        # We shouldn't hit this limit but let's keep things calm when running batches
        time.sleep(0.2)

    # Write the updated addresses to a new CSV file
    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as csvfile:
        fieldnames = ADDRESS_SEARCH_FIELDS + ADDRESS_MATCH_FIELDS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for address in addresses:
            writer.writerow(address)

    print(f"Matched {matches} addresses out of {len(addresses)}")


run()
