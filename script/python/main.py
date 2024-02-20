import requests, pandas, os
from requests.auth import HTTPBasicAuth

# change DEV by True to limit request by 5 max. This avoid to many API request and to many cash flow
DEV = False
print("PYTHON PROCESS.....START")
# Change this path to save file as needed
OUTPUT_CSV_PATH = os.getenv('GGl_PLACES_CSV')

# To replace by your own API key
GGL_API_KEY = os.getenv('GGL_API_KEY')
# To replace by your own geoserver user name to request auth
GEOSERVER_USER = os.getenv('EDP_GEOSERVER_USER')
# To replace by your own geoserver user password to request auth
GEOSERVER_PWD = os.getenv('EDP_GEOSERVER_PASSWORD')
# To replace by your own geoserver URL
# "https://edp.jdev.fr/geoserver/edp/ows"
GEOSERVER_URL = os.getenv('EDP_GEOSERVER_URL')
# Adapt layer name
# "edp:commerce"
LAYER_NAME = os.getenv('EDP_COMMERCE_LAYER')

URL = (
    GEOSERVER_URL
    + "?service=WFS&version=1.0.0&request=GetFeature&typeName="
    + LAYER_NAME
    + "&outputFormat=application%2Fjson"
)

rows = []
days = {
    1: "lundi",
    2: "mardi",
    3: "mercredi",
    4: "jeudi",
    5: "vendredi",
    6: "samedi",
    8: "dimanche",
}


# Request with authent info
headers = {"Accept": "application/json"}
auth = HTTPBasicAuth(GEOSERVER_USER, GEOSERVER_PWD)
response = requests.get(URL, auth=auth, headers=headers)
# Read WFS response
responseJson = response.json()
features = responseJson["features"]


'''
Create API URL request
'''
def get_url(place_id):
    place_api_url = "https://places.googleapis.com/v1/places/" + place_id
    place_api_url += "?fields=id,displayName,regularOpeningHours,location"
    place_api_url += "&key=" + GGL_API_KEY
    return place_api_url

'''
Read API response and format to CSV row
'''
def create_json(details_json):
    regOpeningHours = details_json["regularOpeningHours"]
    periods = regOpeningHours["periods"]
    json_place = {
        "latitude": details_json["location"]["latitude"],
        "longitude": details_json["location"]["longitude"],
        "name": details_json["displayName"]["text"],
        "id": details_json["id"],
        "weekdescribe": regOpeningHours["weekdayDescriptions"]
    }
    for period in periods:
        # day number
        day_number = period["open"]["day"]
        field_open = str(day_number) + "_open"
        field_close = str(day_number) + "_close"
        # convert time to minutes (12h30 -> 12h*60min +30 -> 750 min)
        # this allow to find easily if opening now. Field name contain day value (e.g 3 is Wednesday).
        # ========
        # Example :
        # ========
        # A restaurant is open from 12h30 (750 min) to 14h30 (870 min) 
        # If we request at 13h00 (780 min) a wednesday if restaurant is open :
        # YES -> 750 <= 780 <= 870 -> Restaurant is open at this time !

        minutes_open = (period["open"]["hour"]*60) + period["open"]["minute"]
        minutes_close = (period["close"]["hour"]*60) + period["close"]["minute"]
        if not field_open in json_place:
            json_place[field_open] = []
        if not field_close in json_place:
            json_place[field_close] = []
        json_place[field_open].append(minutes_open)
        json_place[field_close].append(minutes_close)

    return json_place

'''
Loop over features to get each API places infos by feature place id
'''
i = 0
for feature in responseJson["features"]:
    if i > 0 and DEV is True:
        break
    props = feature["properties"]
    place_id = props["google_id"]
    request_url = get_url(place_id)
    response_details = requests.get(request_url)
    details_json = response_details.json()
    if "regularOpeningHours" in details_json:
        row = create_json(details_json)
        rows.append(row)
    i+=1

# create dataframe
dataframe = pandas.json_normalize(rows)
# save CSV file
print("SAVE CSV : " + OUTPUT_CSV_PATH)
dataframe.to_csv(OUTPUT_CSV_PATH, encoding='utf-8')
print("PYTHON PROCESS.....FINISH")
