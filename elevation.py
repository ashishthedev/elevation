###########################################################
## Bottle server for elevation service
## 2016-Feb-16 Tue 01:57 PM
###########################################################

import bottle
from bottle import run, response
import fnmatch
import json
import gdal
import os
import logging

logging.basicConfig(filename='elevation.log', format=logging.BASIC_FORMAT, level=logging.DEBUG)
logging.info('_'*70)
logging.info("SERVER RESTARTED")
logging.info('_'*70)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UNZIPPED_RAW_DATA_DIR = os.path.join(BASE_DIR, "rawData", "unzippedAdfFiles")
FILE_FORMAT = "hdr.adf"

KNOWN_NO_DATA_VALUES = [
        #Sometimes, we are unable to pythonically read no data values, but the binary utility still reports the correct no data value. For those cases, known no data values can be supplied here.
"-3.40282346638529e+38",
]

# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

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
    logging.info("_"*70)
    for filename in getGlobbedFiles():
        noDataValue = GetNoDataValueForFile(filename)
        elevation = searchElevationForLatLngInFile(filename, lat, lng)
        if elevation and elevation != noDataValue and elevation not in KNOWN_NO_DATA_VALUES:
            logging.info("Found elevation {} in file {}".format(elevation, filename))
            return elevation
    else:
        return "NA"

app = bottle.default_app()
gdal.AllRegister()

@app.route('/')
def index():
    return '<pre>Elevation Service Running</pre>'

@app.route('/elevation/lat/<lat>/lng/<lng>')
@enable_cors
def elevation(lat, lng):
    logging.info("_"*70)

    response.content_type = 'application/json'
    return json.dumps({
        "elevation": searchElevationForLatLng(lat, lng)
        })

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, reloader=True, debug=True)

