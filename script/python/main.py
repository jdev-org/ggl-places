import requests, pandas, os, sys, json, logging
from requests.auth import HTTPBasicAuth
from places_utils import create_row, get_places_to_json, get_error_place_to_json
from const import ENCODING

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S ")

LIMIT = None
if len(sys.argv) > 1 and sys.argv[1]:
    # change DEV by True to limit request by 5 max. This avoid to many API request and to many cash flow
    LIMIT = int(sys.argv[1])

logging.info("PYTHON PROCESS.....START")
# Change this path to save file as needed
OUTPUT_CSV_PATH = os.getenv("GGl_PLACES_CSV")
# JSON File
OUTPUT_JSON_PATH = os.getenv("GGl_PLACES_JSON")
# Will contains ids not processed because of no google place id
OUTPUT_JSON_PATH_ERROR = OUTPUT_JSON_PATH + ".error.json"
# To replace by your own API key
GGL_API_KEY = os.getenv("GGL_API_KEY")
# To replace by your own geoserver user name to request auth
GEOSERVER_USER = os.getenv("EDP_GEOSERVER_USER")
# To replace by your own geoserver user password to request auth
GEOSERVER_PWD = os.getenv("EDP_GEOSERVER_PASSWORD")
# To replace by your own geoserver URL
# "https://edp.jdev.fr/geoserver/edp/ows"
GEOSERVER_URL = os.getenv("EDP_GEOSERVER_URL")
# Adapt layer name
# "edp:commerce"
LAYER_NAME = os.getenv("EDP_COMMERCE_LAYER")

URL = (
    GEOSERVER_URL
    + "?service=WFS&version=1.0.0&request=GetFeature&typeName="
    + LAYER_NAME
    + "&outputFormat=application%2Fjson"
)

# Request with authent info
headers = {"Accept": "application/json"}
auth = HTTPBasicAuth(GEOSERVER_USER, GEOSERVER_PWD)
response = requests.get(URL, auth=auth, headers=headers)
# Read WFS response
responseJson = response.json()
features = responseJson["features"]

api_response_json = {"markets": []}

"""
Loop over features to create json with API places infos
And open created file.
"""
if not os.path.exists(OUTPUT_JSON_PATH):
    get_places_to_json(features, OUTPUT_JSON_PATH, LIMIT)

json_places_file = open(OUTPUT_JSON_PATH)
places_data = json.load(json_places_file)
places = places_data["places"]

"""
Loop over features to get features without API place id.
The features will not be processed.

"""
wrong_places_id = []
if "places_error" in places_data:
    places_error = places_data["places_error"]
    for wrong_place in places_error:
        wrong_places_id.append(wrong_place["id"])
else:
    places_error = []
get_error_place_to_json(features, places_error, OUTPUT_JSON_PATH_ERROR)


"""
Loop over features to get each API places infos by feature place id
"""
i = 0
rows = []
for feature in features:
    props = feature["properties"]
    location = {"longitude": props["lon"], "latitude": props["lat"]}
    place_id = props["google_id"]
    if not place_id or place_id in wrong_places_id:
        continue

    # get place info from json
    def find_place(read_place):
        return read_place["id"] == place_id

    place_result = filter(find_place, places)
    place_list = list(place_result)
    # Warning : will be not found if feature place ID was not processed (LIMIT param)
    if not place_list:
        continue
    place = place_list[0]
    place["location"] = location

    if "regularOpeningHours" in place:
        row = create_row(place)
        rows.append(row)

# create dataframe
dataframe = pandas.json_normalize(rows)
# save CSV file
logging.info("SAVE CSV : " + OUTPUT_CSV_PATH)
dataframe.to_csv(OUTPUT_CSV_PATH, encoding=ENCODING)
logging.info("PYTHON PROCESS.....FINISH")
