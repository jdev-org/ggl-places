# ggl-places

## What ?

This repo contain some scripts to update database market hours from google place ID.

## Prerequisite

We needs :

- market datasource (with google place id field at least) from geoserver WFS
- google place /detail API KEY to request hours for each market
- PostGreSQL/PostGIS and user access (will be use to create and write a table)

Some packages will be installed by `install.sh` script :

https://github.com/jdev-org/ggl-places/blob/cbf46226d84fd8b731724a8d51cf7c2331238c8b/script/python/install.sh#L9-L12

## Install

* Open `start.sh` and change env variables values :

https://github.com/jdev-org/ggl-places/blob/0d72c1bfaf06646104f52a7aa0cbf8b1e68a77f7/start.sh#L9-L18

* To start the process, use this command with a classic (Linux) terminal :

`. ./start.sh`

Note that : 
>You will find a `.venv` in `script/python/` (python3)
>
>Process will automatically save a new `place_hours.csv` into `root` directory
>
> Process will automatically create (or overwrite) a PostGIS table


## And now ?

**Publish this new table with your favorite GIS server (e.g GeoServer)**


## Data model explain

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


