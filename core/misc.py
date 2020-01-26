import gdal
import fnmatch
import os
import time
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
            logging.info("{} - Found elevation {} in file {}".format(time.time(), elevation, filename))
            return elevation
    else:
        return "NA"