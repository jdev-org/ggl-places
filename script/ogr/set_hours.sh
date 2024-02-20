#!/bin/bash

# Change SRS options or others if needed
ogr2ogr -overwrite -nlt POINT -f PostgreSQL PG:"host=localhost user=myuser dbname=mydbname password=mysecret"  $1 -s_srs EPSG:4326 -t_srs EPSG:4326  -oo AUTODETECT_TYPE=YES  -lco OVERWRITE=yes -lco GEOMETRY_NAME=geom -oo X_POSSIBLE_NAMES=longitude -oo Y_POSSIBLE_NAMES=latitude