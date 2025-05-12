import requests

# Use your OS API key from the OS Data Hub, a string of 32 characters
# Note: The API key should be kept secret and not shared publicly
YOUR_OS_API_KEY = 'YOUR_OS_API_KEY'


def fetch_data_from_os_api(collection, ids, id_type):
    # fetch data from OS API based on collection name and IDs.

    os_ngd_url = f"https://api.os.uk/features/ngd/ofa/v1/collections/{collection}/items"
    filter_units = [f"({id_type}='{id}')" for id in ids]
    filter_string = 'or'.join(filter_units)
    parameters = {
        "key": YOUR_OS_API_KEY,
        "filter": filter_string
    }
    return requests.get(url=os_ngd_url, params=parameters, timeout=10).json()


# Here we use a sample OSID to demonstrate the process
OSIDS = ['a3677768-e3fc-45ca-b033-66c8e749aa98']
# we know this OSID is in the sites collection
data = fetch_data_from_os_api("lus-fts-site-2", OSIDS, "osid")

UPRNs_to_join = []
if data['features']:
    for feature in data['features']:
        if 'sitetoaddressreference' in feature['properties']:
            uprn_references = feature['properties']['sitetoaddressreference']
            for uprn_reference in uprn_references:
                uprn = uprn_reference['uprn']
                UPRNs_to_join.append(uprn)
print("these are the uprns:", UPRNs_to_join)

road_link_toids = []
linked_id_params = {"key": YOUR_OS_API_KEY}
for uprn in UPRNs_to_join:
    data = requests.get(f"https://api.os.uk/search/links/v1/featureTypes/BLPU/{uprn}", params=linked_id_params,
                        timeout=10).json()
    for correlation in data["correlations"]:
        if correlation["correlatedFeatureType"] == "RoadLink":
            for identifier in correlation["correlatedIdentifiers"]:
                road_link_toids.append(identifier["identifier"])

# The NGD collection name and version e.g. "trn-ntwk-roadlink-4"

road_link_data = fetch_data_from_os_api("trn-ntwk-roadlink-4", road_link_toids, 'toid')

roadtrackorpath_ids = []
for feature in road_link_data["features"]:
    for reference in feature["properties"].get("roadtrackorpathreference", []):
        roadtrackorpath_ids.append(reference["roadtrackorpathid"])
print("these are the IDs for the road track and path features :", roadtrackorpath_ids)

# The NGD collection name and version e.g. "trn-fts-roadtrackorpath-3"
NGD_COLLECTION = "trn-fts-roadtrackorpath-3"
road_track_and_path_data = fetch_data_from_os_api(NGD_COLLECTION, roadtrackorpath_ids, 'osid')

print(road_track_and_path_data)
