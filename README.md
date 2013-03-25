osm_maps
========

How to generate a worldwide, general purpose, tms tiled map. Based on Open Street Map and SRTM data. 

### Tools:
* [osm-bright](https://github.com/mapbox/osm-bright)
* [imposm](http://imposm.org/docs/imposm/latest/)

### Step 1: download osm data and load it into a PostGIS database.

Data download links can be found here: [Planet.osm](http://wiki.openstreetmap.org/wiki/Planet.osm)
For a worldwide dump: [planet](ftp://ftp.spline.de/pub/openstreetmap/pbf/)
Save the planet.pbf to a folder with loads of space (the file is about 20Gb).

Create a new PostGIS database. For such a huge database it is strongly 
suggested to tune your Postgresql configuration settings: [see here](http://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server). On Ubuntu Postgreswql configuration file is found here: `/etc/postgresql/9.1/main/postgresql.conf`

Install Imposm. [Here](http://imposm.org/docs/imposm/latest/install.html) are 
some detailed installation instructions. You might want to create a python 
virtualenv where to install all your osm dependencies.

Clone [osm-bright](https://github.com/mapbox/osm-bright)

At this point you need to follow the instructions on 
[osm-bright](https://github.com/mapbox/osm-bright) for setting up the PostGIS 
database, and in particular you need to follow the imposm instructions. In particular you will need to reference [imposm-mapping.py](https://github.com/mapbox/osm-bright/blob/master/imposm-mapping.py).

```sh
imposm --read --write --concurrency 6 -m imposm-mapping.py --optimize --deploy-production-tables --connection postgis://<postgres_user>:<postgres_password>@localhost/<postgis_database> ~/Downloads/osm/planet-130102.osm.pbf
```
This will take some time (several hours!) and will create some big cache files, 
that if disk space is needed, can be deleted after the command terminates and 
all the data is correctly loaded on the database.








