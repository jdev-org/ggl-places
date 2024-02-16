import requests

GEOSERVER_URL = "https://edp.jdev.fr/geoserver/edp/ows"
LAYER_NAME = "edp:commerce"
URL = GEOSERVER_URL + "?service=WFS&version=1.0.0&request=GetFeature&typeName=" + LAYER_NAME + "&outputFormat=application%2Fjson"

from requests.auth import HTTPBasicAuth

headers = {'Accept': 'application/json'}

auth = HTTPBasicAuth('', '')

response = requests.get(URL, auth=auth, headers=headers)

responseJson = response.json()
features = responseJson["features"]

for feature in responseJson["features"]:
    props = feature["properties"]
    place_id = props["google_id"]

