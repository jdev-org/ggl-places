# ggl-places

## What ?

This repo contain some scripts to update database market hours from google place ID.

## Prerequisite

We needs :

- market datasource (with google place id field at least) from geoserver WFS
- google place /detail API KEY to request hours for each market
- ogr2ogr (gdal) installed
- PostGreSQL/PostGIS and user access (will be use to create and write a table)

## Install

* Open start.sh and change env variables values :

https://github.com/jdev-org/ggl-places/blob/0d72c1bfaf06646104f52a7aa0cbf8b1e68a77f7/start.sh#L9-L18

* Start process with a classic (Linux) terminal :

`. ./start.sh`

> You will find a `.venv` in `script/python/` (python3)

> Process will automatically save a new `place_hours.csv` into `root` directory

> Process will automatically create (or overwrite) a PostGIS table

* Publish this layer with GeoServer (or what you need) <-> PostGIS Table

