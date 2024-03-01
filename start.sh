#!/bin/bash
echo "PROCESS.....START"

refresh_file="$1"
install_env="$2"

env_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#########
# ENV vars :
# SET OR CHANGE THIS FIRST  (used by Python script)
#########

# If needeed, uncomment and adapta this line to use a config.sh file
# . /srv/script/config.sh

# You can override this two file path to use full path as /srv/sctipt/gg-places/place_hours.csv
export GGl_PLACES_CSV="$env_dir/place_hours.csv"
# You can override this file path to use full path as /srv/sctipt/gg-places/places.json
export GGl_PLACES_JSON="$env_dir/places.json"

# If necessary, adapt or comment vars if you use a config.sh file

# Required vars
export GGL_API_KEY=""
export EDP_GEOSERVER_USER=""
export EDP_COMMERCE_LAYER=""

# Not required if layer is not protected
export EDP_GEOSERVER_PASSWORD=""
export EDP_GEOSERVER_URL=""

# Required DB vars
export EDP_DB_NAME=""
export EDP_DB_HOST=""
export EDP_DB_USER=""
export EDP_DB_PASSWORD=""

install_script="$env_dir/script/python/install.sh"
ogr_script="$env_dir/script/ogr/set_hours.sh"
venv_path="$env_dir/script/python/.venv"
process_file="$env_dir/script/python/main.py"

json_file_place="$env_dir/places.json"

###########
# PROCESS
###########

if [ $refresh_file = "true" ] && [ -f "$json_file_place" ]
then
    rm $json_file_place
else
    echo "KEEP PLACES FILE : $json_file_place"
fi

# install
if [ $install_env = "true" ]
then
    . "$install_script"
fi

# use venv to get api infos
. "$venv_path/bin/activate"
python "$process_file"
deactivate

echo "CREATE OR UPDATE LAYER....."
# load postgis table
. "$ogr_script"

echo "PROCESS.....SUCCESS !"
