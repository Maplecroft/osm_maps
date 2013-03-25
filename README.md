osm_maps
========

How to generate a worldwide, general purpose, tms tiled map. Based on [Open Street Map](http://www.openstreetmap.org/) and [SRTM](http://srtm.csi.cgiar.org/) data. 

### Tools you will need to have installed:
* [osm-bright](https://github.com/mapbox/osm-bright)
* [imposm](http://imposm.org/docs/imposm/latest/)
* [mapproxy](http://mapproxy.org/) (with [mapnik](http://mapnik.org/))
* [tilemill](http://mapbox.com/tilemill/)

### Step 1: download osm data and load it into a PostGIS database.

OSM data download links can be found here: [Planet.osm](http://wiki.openstreetmap.org/wiki/Planet.osm) (for a worldwide dump: [planet](ftp://ftp.spline.de/pub/openstreetmap/pbf/)).
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
up the PostGIS database, and in particular the imposm related instructions. Short version: you will need to reference this file from the osm-bright repo: [imposm-mapping.py](https://github.com/mapbox/osm-bright/blob/master/imposm-mapping.py) 
in your imposum command.

With everything setup correctly, this will load the Planet.osm dump into postGIS:

```sh
imposm --read --write --concurrency 6 -m imposm-mapping.py --optimize --deploy-production-tables --connection postgis://<postgres_user>:<postgres_password>@localhost/<postgis_database> ~/Downloads/osm/planet-130102.osm.pbf
```
A detailed explanation of what is happening here can be found on the imposm [tutorial](http://imposm.org/docs/imposm/latest/tutorial.html#create-database) page.

This will take some time (several hours!) and will create some big cache files. 
If disk space is needed, these can be deleted after the command terminates and 
all the data is correctly loaded into the database.








