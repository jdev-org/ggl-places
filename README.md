> This scripts works with Linux

> You need to adapt `.sh` scripts to works out of Linix OS

# ggl-places

## What ?

This repo contain some scripts to update database market hours from google place ID.

## Prerequisite

We needs :

- market datasource (with google place id field at least) from geoserver WFS
- google place /detail API KEY to request hours for each market
- PostGreSQL/PostGIS and user access (will be use to create and write a table)

Some packages will be installed by `install.sh` script :

https://github.com/jdev-org/ggl-places/blob/main/script/python/install.sh

## Install

If the process use a root or sudo user, you just have to go to the next section because install process is includes in `start.sh` file (need super user right to install dependancies).

If you use a non superuser to trigger `start.sh` file, you have to use `install.sh` first to install dependancies and python virtual env :

https://github.com/jdev-org/ggl-places/blob/main/script/python/install.sh

**Commands :**
- cd script/python
- sudo bash install.sh

Go to the next section to start the process.


## Process

First, open `start.sh` and change environment variables values :

https://github.com/jdev-org/ggl-places/blob/334ca1541ec7ddac26489b32a7a8462db64b9934/start.sh#L13-L22

Next, you can start the process with this (Linux) command :

> [CREATE_FILE] : `<boolean>` - `true` to force places file generation, `false` to use current and don't call API
> [INSTALL] : `<boolean>` - `true` to install (need superuser) or not (if already done or trigger without superuser)

`. ./start.sh [CREATE_FILE] [INSTALL]`

### Process important information

- You will find a `.venv` in `script/python/` directory (python3)

- Process will automatically save a new `place_hours.csv` into `root` directory

- Process will automatically create (or overwrite) a PostGIS table (name is same as CSV file)

- Process will create a new `./places.json` file to allow to read API response if you don't need to request all every time

- Process will create a `./places.json.error.json` file to list feature without API ID and invalid API IDs

- API URI is located in `./script/python/const.py`

- Var env GEOSERVER_USER and GEOSERVER_PASSWORD are not required

## And now ?

**Publish this new table with your favorite GIS server (e.g GeoServer)**

## Data model explainations

* Hours fields (close/open) are show in minutes to ease comparison and conversion :
`12h30 = 12h*60min +30 = 750 min`

* A day is identify by a number :

| Monday    | 1   |
|-----------|-----|
| wednesday | 3   |
| Tuesday   | 2   |
| ...       | ... |
|           |     |

* For a day, table contain many open periods and many close period

```
1_open : [720,1140], -> Monday : 2 open/close periods
1_close: [840,1320], -> Monday : open/closed : 12h-14h and 19h-22h
2_open: [], -> Tuesday : Closed
2_close: [] -> Tuesday : Closed
3_open: [540] -> Wednesday : open at 9h during 1 period
3_close: [1020] -> Wednesday : close at 17h
```

## How to read open/close periods ?

A restaurant is open the monday on 2 periods : 12h-14h and 19h-22h.
In minutes, this will be : 720-840 and 1140-1320

In the table, we will find these values in 2 fields grouped by open or close time : 
```
1_open : [720,1140]
1_close: [840,1320]
```

If we need to know if this restaurant is open at 13h00 :

- Convert 13h00 to minutes ->  780
- Identify day (for this example we use monday) -> 1
- Call server by this restaurant ID
- Read response and fields 1_open, 1_close
- Control that `780` is between `720 <-> 840` or `1140 <-> 1320`
- 780 min is between first period for the monday, so the restaurant is `OPEN` !


