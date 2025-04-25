var collectionId = 'bld-fts-building-4';
var parameters = {}

function osidsToFilterString(osids) {
    let filterUnits = Array.from(osids, (id) => `(osid='${id}'`);
    let filterString = filterUnits.join('or');
    return filterString;
}

const queryString = new URLSearchParams(queryParameters).toString();

// Construct the NGD Features API request URL.
const url = `https://api.os.uk/features/ngd/ofa/v1/collections/${collectionId}/items`;
const fullUrl = `${url}?${queryString}`;

// Fetch features from the API endpoint.
const features = await fetch(url, param).then(response => response.json());
