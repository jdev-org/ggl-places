#!/bin/bash
echo "PROCESS.....START"

env_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create env var
# SET OR CHANGE THIS FIRST  : Python script use them
export GGl_PLACES_CSV="$env_dir/place_hours.csv"
export GGl_PLACES_JSON="$env_dir/places.json"

export GGL_API_KEY = ""
export EDP_GEOSERVER_USER = ""
export EDP_GEOSERVER_PASSWORD = ""
export EDP_GEOSERVER_URL = ""
export EDP_COMMERCE_LAYER = ""

export EDP_DB_NAME = ""
export EDP_DB_HOST = ""
export EDP_DB_USER = ""
export EDP_DB_PASSWORD = ""

install_script="$env_dir/script/python/install.sh"
ogr_script="$env_dir/script/ogr/set_hours.sh"
venv_path="$env_dir/script/python/.venv"
process_file="$env_dir/script/python/main.py"

# install
. "$install_script"
# use venv to get api infos
. "$venv_path/bin/activate"
python "$process_file"
deactivate
echo "CREATE OR UPDATE LAYER....."
# load postgis table
. "$ogr_script"
echo "PROCESS.....SUCCESS !"