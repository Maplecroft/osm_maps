osm_maps
========

How to generate a worldwide, general purpose, tms tiled map. Based on [Open Street Map](http://www.openstreetmap.org/) and [SRTM](http://srtm.csi.cgiar.org/) data. 

Note: if you want to give it a go at customizing map styles in tilemill, I suggest
applying these notes first to a small region of the world and when happy apply it to
the whole world. This way tilemill will re-render things much faster.

### Tools you will need to have installed:
* [osm-bright](https://github.com/mapbox/osm-bright)
* [imposm](http://imposm.org/docs/imposm/latest/)
* [mapproxy](http://mapproxy.org/) (with [mapnik](http://mapnik.org/))
* [tilemill](http://mapbox.com/tilemill/)

### Step 1: download osm data and load it into a PostGIS database.

OSM data download links can be found here: [Planet.osm](http://wiki.openstreetmap.org/wiki/Planet.osm). For a worldwide dump: [planet](http://ftp.spline.de/pub/openstreetmap/pbf/).
Save the planet.pbf of choice to a folder with lots of space (the file is about 20Gb).

Create and tune a new PostGIS database. For such a big database it is strongly 
suggested to tune your Postgresql configuration settings to match your machine capabilities ([see here](http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server) for instructions). On 
Ubuntu the Postgresql configuration file can be found here: `/etc/postgresql/9.1/main/postgresql.conf`.

Install Imposm. [Here](http://imposm.org/docs/imposm/latest/install.html) are 
some detailed installation instructions. You might want to create a python 
virtualenv where to install all of your python osm-related dependencies.

Clone [osm-bright](https://github.com/mapbox/osm-bright).

At this point you need to follow the instructions on the
[osm-bright](https://github.com/mapbox/osm-bright) README page for setting 
up the PostGIS database, and in particular the imposm related instructions. Short version: you will need to reference this file from the osm-bright repo, [imposm-mapping.py](https://github.com/mapbox/osm-bright/blob/master/imposm-mapping.py), 
in your imposum command.

With everything setup correctly, this will load the Planet.osm dump into postGIS:

```sh
imposm --read --write --concurrency 6 -m imposm-mapping.py --optimize --deploy-production-tables --connection postgis://<postgres_user>:<postgres_password>@localhost/<postgis_database> ~/Downloads/osm/planet-130102.osm.pbf
```
A detailed explanation of what is happening here can be found on the imposm [tutorial](http://imposm.org/docs/imposm/latest/tutorial.html#create-database) page.

This will take some time (several hours!) and will create some big cache files too. 
If disk space is needed, these can be deleted after the command terminates and 
all the data is correctly loaded into the database.


### Step 2: download and set-up the [SRTM](http://srtm.csi.cgiar.org/) 90m Digital Elevation Data for the entire world.

Attention: `make.py` expects lots of free disk space!

Note: the following steps assume that you have the relevant gdal tools correctly 
installed on your system.

[Here](http://www.ambiotek.com/srtm) you can download a kmz file that represents
an overview of all the data.

To download the data all at once you can try something like:
```sh
wget -m ftp://anonymous@srtm.csi.cgiar.org/SRTM_v41/SRTM_Data_GeoTIFF/\* .
```

This will take several hours and almost certainly it will fail for some tiles. So,
after this, you will need to go back and explicitly download what is still missing.
Something like:
```sh
wget -m ftp://anonymous@srtm.csi.cgiar.org/SRTM_v41/SRTM_Data_GeoTIFF/srtm_36_02.zip .
```

To create an shapefile index of what has been downloaded (after unzipping!):
```sh
gdaltindex unwarp_index.shp *.tif
```

Processing tools for the srtm data can be fond in the srtm folder. In particular:
* `make.py` will prepare the colour-relief rasters.
* `configure.py` is a configuration file for paths used in `make.py`. This needs to be edited and the relevant folders need to be created.
* `make_project_frag.py` is a script to make an `.mml` fragment to insert into 
tilemill's main `.mml` project file (the one generated from the `osm-bright` repo).


### Step 3: set-up the customized [osm-bright](https://github.com/mapbox/osm-bright) tilemill project.

This is a 2 steps process.
First we need to follow the instructions on the README file of the osm-bright repo. 
In particular, arrived at this point, you will need to look at points 3 and 4.
It assumes you have [tilemill](http://mapbox.com/tilemill/) up and running.

Important note: tilemill mite take a very long time to render this project.

One way to get tilemill up and running after successful installation: 
```sh
/usr/share/tilemill/index.js --server=true
```

Once you manage to see your openstreet data rendered in tilemill, we are ready to
customize it with the srtm data.




