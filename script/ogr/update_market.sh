#!/bin/bash

# Change SRS options or others if needed
# By default SRS is EPSG:2154
DB="$EDP_DB_NAME"
USER="$EDP_DB_USER"
HOST="$EDP_DB_HOST"
PWD="$EDP_DB_PASSWORD"

ogr2ogr -overwrite -nlt POINT -f PostgreSQL PG:"host=$HOST user=$USER dbname=$DB password=$PWD"  $1 -s_srs EPSG:2154 -t_srs EPSG:2154  -lco SPATIAL_INDEX=GIST -oo AUTODETECT_TYPE=YES  -lco OVERWRITE=yes -lco GEOMETRY_NAME=geom -oo X_POSSIBLE_NAMES=longitude -oo Y_POSSIBLE_NAMES=latitude
