import gdal
import fnmatch
import os
import datetime
import logging
import argparse
import sys

logging.basicConfig(filename='elevation_prog.log', format=logging.BASIC_FORMAT, level=logging.DEBUG)
logging.info('_'*70)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UNZIPPED_RAW_DATA_DIR = os.path.join(BASE_DIR, "rawData", "unzippedAdfFiles")
FILE_FORMAT = "hdr.adf"

KNOWN_NO_DATA_VALUES = [
        #Sometimes, we are unable to pythonically read no data values, but the binary utility still reports the correct no data value. For those cases, known no data values can be supplied here.
"-3.40282346638529e+38",
]

def getGlobbedFiles():
    matches = []
    for root, dirnames, filenames in os.walk(UNZIPPED_RAW_DATA_DIR):
        for filename in fnmatch.filter(filenames, FILE_FORMAT):
            matches.append(os.path.join(root, filename))
    return matches

def searchElevationForLatLngInFile(filename, lat, lng):
    import subprocess
    gdallocationinfo = "/usr/bin/gdallocationinfo"
    valonly = "-valonly"
    geoloc = "-geoloc"
    wgs84 = "-wgs84"
    cmd = [gdallocationinfo, valonly, geoloc, wgs84, filename, lng, lat ] #Note: lat=y; lng=x
    elevation = subprocess.check_output(cmd)
    elevation = elevation.rstrip()#Remove the "\n" in the end
    return elevation


def GetNoDataValueForFile(filename):
    ds = gdal.Open(filename, gdal.GA_ReadOnly)
    if ds is None:
        raise Exception("Could not open {}".format(filename))

    return str(ds.GetRasterBand(1).GetNoDataValue())


def searchElevationForLatLng(lat, lng):
    for filename in getGlobbedFiles():
        noDataValue = GetNoDataValueForFile(filename)
        elevation = searchElevationForLatLngInFile(filename, lat, lng)
        if elevation and elevation != noDataValue and elevation not in KNOWN_NO_DATA_VALUES:
            logging.info("{} - Found elevation {} for lat: {} and lng: {} in file {}".format(datetime.datetime.now(), elevation, lat, lng, filename))
            return elevation
    else:
        return "NA"

if __name__ == "__main__":
    # python elevation_prog.py --lng 132.255024546978 --lat -12.659170573364879
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--lat', dest='lat', type=str, help='Latitude')
    parser.add_argument('--lng', dest='lng', type=str, help='Longitude')

    args = parser.parse_args()

    try:
        elevation = searchElevationForLatLng(args.lat, args.lng)
        print(elevation)
        exit(0)
    except Exception as ex: #Eat the exception so that real error gets printed and passed back.
        print("Exception: " + str(ex), file=sys.stderr)
        pass
