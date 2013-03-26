#!/usr/bin/env python


import re
import sys
import subprocess
import zipfile
import glob
import os
from json import loads, dumps
from shutil import rmtree, copyfile
from os.path import join, isdir, expanduser, exists
from collections import defaultdict
from subprocess import call

if not exists('./configure.py'):
    sys.stderr.write('Error: configure.py does not exist, did you forget to create it from the sample (configure.py.sample)?\n')
    sys.exit(1)
elif exists('./configure.pyc'):
    os.unlink('./configure.pyc')

from configure import config

sys.path.append('/usr/bin')

if os.path.exists(config["srtm_project"]):
    os.remove(config["srtm_project"])


str = """
    {
      "Datasource": {
        "dbname": "osm_world", 
        "file": "%s", 
        "id": "relief_%s", 
        "project": "osm", 
        "srs": "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
      }, 
      "class": "relief", 
      "id": "relief_%s", 
      "name": "relief_%s",
      "srs": "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs", 
      "status": "on"
    },
"""


with open(config["srtm_project"], "a") as p:
    for r,d,f in os.walk(config["unwarp"]):
        for file in f:
            spl = file.split("_")
            txt = str % ( 
              os.path.join(config["unwarp"], file),
              "_".join([spl[1], spl[2], spl[3]]),
              "_".join([spl[1], spl[2], spl[3]]),
              file.split(".")[0] )
            p.write(txt)