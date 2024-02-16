import requests

GEOSERVER_URL = "https://edp.jdev.fr/geoserver/edp/ows"
LAYER_NAME = "edp:fontaines"
URL = "%s?service=WFS&version=1.0.0&request=GetFeature&typeName=%s&outputFormat=application%2Fjson"(GEOSERVER_URL, LAYER_NAME)

x = requests.get(URL)