#!/usr/bin/env python

from os import path
from collections import defaultdict
config = defaultdict(defaultdict)


config["zip"] = "/home/dbattaglia/gis_data/srtm/srtm.csi.cgiar.org/SRTM_v41/SRTM_Data_GeoTIFF"
config["extract"] = "/home/dbattaglia/gis_data/srtm/extract"
config["merge"] = "/home/dbattaglia/mounts/neptune/gis/srtm/merge"
config["warp"] = "/home/dbattaglia/gis_data/srtm/warp"
config["slope"] = "/home/dbattaglia/gis_data/srtm/slope"
config["color_relief"] = "/home/dbattaglia/gis_data/srtm/color_relief"
config["unwarp"] = "/home/dbattaglia/gis_data/srtm/unwarp"
config["contour"] = "/home/dbattaglia/gis_data/srtm/contour"
config["tile_index"] = "/home/dbattaglia/gis_data/srtm/tile_index"
config["land"] = "/home/dbattaglia/Documents/MapBox/project/OSMBrightWorld2/layers/shoreline_300/ab6b4f6f-shoreline_300.shp"


config["slope_ramp"] = "/home/dbattaglia/gis_data/srtm/slope-ramp.txt"

config["srtm_project"] = "/home/dbattaglia/gis_data/srtm/srtm.mml"
