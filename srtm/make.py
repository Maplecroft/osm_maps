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
import argparse

if not exists('./configure.py'):
    sys.stderr.write('Error: configure.py does not exist, did you forget to create it from the sample (configure.py.sample)?\n')
    sys.exit(1)
elif exists('./configure.pyc'):
    os.unlink('./configure.pyc')

from configure import config

sys.path.append('/usr/bin')


def refresh(folder):
    if os.path.exists(config[folder]):
      rmtree(config[folder])
    os.makedirs(config[folder])


def extract_all( args, dirname, filenames ):
    """
    Called from os.path.walk
    First it removes old unzipped files.
    Then it unzippes all filenames.
    """
    rmtree(config["extract"])
    print "Extracting zip files to %s" % config["extract"]
    for filename in filenames:
        if filename.endswith(".zip"):
            dest = os.path.join(config["zip"], filename)
            try:
                zip_ref = zipfile.ZipFile( dest, 'r' )
                zip_ref.extractall(config["extract"])
                zip_ref.close()
            except zipfile.BadZipfile:
                print "ERROR on: %s" % filename


def get_next_file(column, row):
    new_file = "srtm_%02d_%02d.tif" % (column, row)
    if os.path.exists( os.path.join(config["extract"], new_file) ):
        return new_file
    else:
        return False


def contour():
    """
    Creates a contour shapefile from the elevation model.
    Useful after zoom-levels 12-13, when the elevation model becomes
    too low-res to render nicely.
    150.0 referes to the meters between contour lines. 
    This value can be optimized.
    """
    print "Creating contours"
    refresh("contour")
    for r,d,f in os.walk(config["merge"]):
        for file in f:
            pr = "gdal_contour -a ELEV -i 150.0 %s %s" % (
                os.path.join(config["merge"], file),
                os.path.join(config["contour"], file.replace(".tif", ".shp"))
            )
            subprocess.call(pr, shell=True)


def warp(folder=config["extract"]):
    """
    Reprojecting from WGS84 (EPSG:4326) to Mercatore (EPSG:3785),
    because gdaldem needs to handle meter values, and not lat-longs,  
    when creating slopes and colour-reliefs!
    """
    print "Warping", folder
    for r,d,f in os.walk(folder):
        for file in f:
            if file.endswith(".tif"):
                out = "%s_warp.tif" % file.split(".")[0]
                #final = "%s_slope_color_relief_wgs_84.tif" % out.split(".")[0]
                #if not os.path.exists( os.path.join(config["unwarp"], final) ):
                pr = "gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3785 -wm \
                     200 -multi -dstnodata -32768 -of GTiff %s %s" % (
                      os.path.join(folder, file),
                      os.path.join(config["warp"], out))
                subprocess.call(pr, shell=True)
                slope(out)


def slope(file):
    print "Slope"
    out = "%s_slope.tif" % file.split(".")[0]
    pr = "gdaldem slope %s %s"  % (
      os.path.join(config["warp"], file),
      os.path.join(config["slope"], out) ) 
    subprocess.call(pr, shell=True)
    os.remove(os.path.join(config["warp"], file))
    color_relief(out)
    

def color_relief(file):
    print "color_relief"
    out = "%s_color_relief.tif" % file.split(".")[0]
    pr = "gdaldem color-relief %s %s %s"  % (  #-co compress=lzw
      os.path.join(config["slope"], file),
      config["slope_ramp"],
      os.path.join(config["color_relief"], out) ) 
    subprocess.call(pr, shell=True)
    os.remove(os.path.join(config["slope"], file))
    unwarp(out)
    # more...


def unwarp(file):
    """
    Reprojecting the colour-relief back to lat-long.
    """
    print "unwarp"
    out = "%s_wgs_84.tif" % file.split(".")[0]
    pr = "gdalwarp -s_srs EPSG:3785 -t_srs EPSG:4326 -wm \
         200 -multi -of GTiff %s %s" % ( 
          os.path.join(config["color_relief"], file),
          os.path.join(config["unwarp"], out))
    #os.remove(os.path.join(config["color_relief"], file))
    subprocess.call(pr, shell=True)


def walk(folder):
    for r,d,f in os.walk(config[folder]):
        for file in f:
            locals()[folder](file)


#os.path.walk( config["zip"], extract_all, None )


def main(args):
    task = args.task
    folder = config[args.folder]
    if task == "warp":
        refresh("warp")
        refresh("slope")
        refresh("color_relief")
        refresh("unwarp")

    globals()[task]()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage=("Generate statistics about how HTML tags are used."))
    parser.add_argument("-t", "--task", dest="task", action="store",
        help="Please pass me the name of the task. Options are: \
        warp, merge, contour, extract")
    parser.add_argument("-f", "--folder", dest="folder", action="store",
        help="Folder")
    # Print some help is we do not pass a filename.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    main(args)
