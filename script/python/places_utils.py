import json, os, requests, logging
from const import GGL_URL

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S ")

GGL_API_KEY = os.getenv("GGL_API_KEY")

"""
Save JSON
"""


def create_json(jsonContent, pathFile):
    # Serializing json
    json_object = json.dumps(jsonContent, indent=4)
    # Writing to sample.json
    with open(pathFile, "w") as outfile:
        outfile.write(json_object)


"""
Create API URL request
"""


def get_url(place_id, key):
    place_api_url = GGL_URL + place_id
    place_api_url += "?fields=id,displayName,regularOpeningHours"
    place_api_url += "&key=" + key
    return place_api_url


"""
For each ids get places details into json content
"""


def get_json_content(ids, limit):
    i = 0
    api_content = {"places": [], "places_error": []}
    for id in ids:
        if limit and i > limit:
            break
        request_url = get_url(id, GGL_API_KEY)
        response_details = requests.get(request_url)
        details_json = response_details.json()
        details_json["index"] = i
        if "error" in details_json:
            code = details_json["error"]["code"]
            logging.warning("(" + str(code) + ") " + details_json["error"]["message"])
            details_json["id"] = id
            api_content["places_error"].append(details_json)
        else:
            api_content["places"].append(details_json)
        i += 1
    return api_content


"""
Read API response and format to CSV row
"""


def create_row(details_json):
    regOpeningHours = details_json["regularOpeningHours"]
    periods = regOpeningHours["periods"]
    json_place = {
        "latitude": details_json["location"]["latitude"],
        "longitude": details_json["location"]["longitude"],
        "name": details_json["displayName"]["text"],
        "id": details_json["id"],
        "weekdescribe": regOpeningHours["weekdayDescriptions"],
    }
    for period in periods:
        # day number
        day_number = period["open"]["day"]

        # convert time to minutes (12h30 -> 12h*60min +30 -> 750 min)
        # this allow to find easily if opening now. Field name contain day value (e.g 3 is Wednesday).
        # ========
        # Example :
        # ========
        # A restaurant is open from 12h30 (750 min) to 14h30 (870 min)
        # If we request at 13h00 (780 min) a wednesday if restaurant is open :
        # YES -> 750 <= 780 <= 870 -> Restaurant is open at this time !

        if "open" in period:
            field_open = str(day_number) + "_open"
            if not field_open in json_place:
                json_place[field_open] = []
            minutes_open = (period["open"]["hour"] * 60) + period["open"]["minute"]
            json_place[field_open].append(minutes_open)
        if "close" in period:
            field_close = str(day_number) + "_close"
            if not field_close in json_place:
                json_place[field_close] = []
            minutes_close = (period["close"]["hour"] * 60) + period["close"]["minute"]
            json_place[field_close].append(minutes_close)

    return json_place


"""
Read features and call request for each IDs
"""


def get_places_to_json(features, filePath, limit):
    ids = []
    for feature in features:
        props = feature["properties"]
        place_id = props["google_id"]
        if props["google_id"]:
            ids.append(place_id)
    json_to_process = get_json_content(ids, limit)
    create_json(json_to_process, filePath)


"""
Usefull to identify features:
- without api ID 
- wrong API IDs (return error on request)
"""


def get_error_place_to_json(features, wrong_places, filePath):
    json_content = {"features_id": [], "api_id": []}
    for feature in features:
        props = feature["properties"]
        if not props["google_id"]:
            json_content["features_id"].append(props["id"])
    for place in wrong_places:
        json_content["api_id"].append(place["id"])
    create_json(json_content, filePath)
