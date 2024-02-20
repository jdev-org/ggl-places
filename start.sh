#!/bin/bash

# Create env var
# SET OR CHANGE THIS FIRST  : Python script use them
export GGl_PLACES_CSV = ""
export GGL_API_KEY = ""
export EDP_GEOSERVER_USER = ""
export EDP_GEOSERVER_PASSWORD = ""
export EDP_GEOSERVER_URL = ""
export EDP_COMMERCE_LAYER = ""

export EDP_DB_NAME = ""
export EDP_DB_HOST = ""
export EDP_DB_USER = ""
export EDP_DB_PASSWORD = ""


# install
. ./script/python/install.sh

# use venv to get api infos
. ./script/python/.venv/bin/activate
python ./script/python/main.py
deactivate

# load postgis table
. ./script/ogr/set_hours.sh