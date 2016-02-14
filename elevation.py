#Bottle server for elevation service.

import bottle
from bottle import Bottle, run, response
import fnmatch
import gdal
import glob
import os
import logging
import time

logging.basicConfig(filename='elevation.log', format=logging.BASIC_FORMAT, level=logging.DEBUG)
logging.info('_'*70)
logging.info("SERVER RESTARTED")
logging.info('_'*70)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UNZIPPED_RAW_DATA_DIR = os.path.join(BASE_DIR, "rawData", "unzippedAdfFiles")
FILE_FORMAT = "*.tif"
FILE_FORMAT = "hdr.adf"

LOOKUP_FILES = [
        (32750, os.path.join(UNZIPPED_RAW_DATA_DIR, "NT5mDEM", "hdr.adf")),
        (32750, os.path.join(UNZIPPED_RAW_DATA_DIR, "NSW5mDEM", "hdr.adf")),
        (32750, os.path.join(UNZIPPED_RAW_DATA_DIR, "QLD5mDEM", "hdr.adf")),
        (32750, os.path.join(UNZIPPED_RAW_DATA_DIR, "VIC5mDEM", "hdr.adf")),
        (32750, os.path.join(UNZIPPED_RAW_DATA_DIR, "WA5mDEM", "hdr.adf")),
        (32750, os.path.join(UNZIPPED_RAW_DATA_DIR, "SA5mDEM", "hdr.adf")),
        ]

def convertLatLngToEastingNorthingsToLatLng(lat, lng, sourceEPSG):
    import ogr
    import osr
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(lat, lng)
    logging.info("Original Point: x:{} y: {}".format(point.GetX(), point.GetY()))

    sourceSR = osr.SpatialReference()
    sourceSR.ImportFromEPSG(sourceEPSG)
    targetSR = osr.SpatialReference()
    targetSR.ImportFromEPSG(4326)

    coordTrans = osr.CoordinateTransformation(sourceSR, targetSR)
    point.Transform(coordTrans)
    lat = point.GetX()
    lng = point.GetY()
    logging.info("New Point: x:{} y: {}".format(point.GetX(), point.GetY()))

    return lat, lng

def convertEastingNorthingsToLatLng(eastings, northings):
    import ogr
    import osr
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(eastings, northings)
    logging.info("Original Point: x:{} y: {}".format(point.GetX(), point.GetY()))

    sourceSR = osr.SpatialReference()
    sourceSR.ImportFromEPSG(32750)
    targetSR = osr.SpatialReference()
    targetSR.ImportFromEPSG(4326)

    coordTrans = osr.CoordinateTransformation(sourceSR, targetSR)
    point.Transform(coordTrans)
    lat = point.GetX()
    lng = point.GetY()
    logging.info("New Point: x:{} y: {}".format(point.GetX(), point.GetY()))

    return lat, lng


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

def getEPSGCodesAndFiles():
    return LOOKUP_FILES

def getFiles():
    matches = []
    for root, dirnames, filenames in os.walk(UNZIPPED_RAW_DATA_DIR):
        for filename in fnmatch.filter(filenames, FILE_FORMAT):
            matches.append(os.path.join(root, filename))
    return matches


app = bottle.default_app()
@app.route('/')
def index():
    return '<pre>Elevation Service Running</pre>'

@app.route('/elevation/lat/<lat>/lng/<lng>')
@enable_cors
def elevation(lat, lng):
    logging.info("_"*70)
    lat = float(lat)
    lng = float(lng)
    elevation = None
    for sourceEPSG, filename in getEPSGCodesAndFiles():
        utmEastings, utmNorthings = convertLatLngToEastingNorthingsToLatLng(lat, lng, sourceEPSG)
        found, x = searchElevationForEastingsAndNorthings(filename, utmEastings, utmNorthings)
        if found:
            elevation = x
            fn = filename
            break
    now = time.time()
    if elevation:
        logging.info("{now}: Elevation: {elevation} at lat:{lat}, lng:{lng} in file:{fn}".format(**locals()))
    else:
        elevation = "NA"
        logging.info("{now}: Elevation data not available for lat:{lat}, lng:{lng}".format(**locals()))

    import json
    response.content_type = 'application/json'

    return json.dumps({
        "elevation": elevation,
        "utmEastings":utmEastings,
        "utmNorthings":utmNorthings,
        })

def searchElevationForEastingsAndNorthings(filename, utmEastings, utmNorthings):
    gdal.AllRegister()
    logging.debug("Reading {}Mb {}".format(os.stat(filename).st_size/(1024*1024), filename))
    ds = gdal.Open(filename, gdal.GA_ReadOnly)

    if ds is None:
        raise Exception("Could not open {}".format(filename))

    #get image size
    bands = ds.RasterCount

    #get georeference info
    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]

    xOffset = int((utmEastings - xOrigin)/pixelWidth)
    yOffset = int((utmNorthings - yOrigin)/pixelHeight)

    found = False
    elevation = None
    for i in range(bands):
        bandIndex = i + 1
        band = ds.GetRasterBand(bandIndex)
        data = band.ReadAsArray(xOffset, yOffset, 1, 1)
        if data:
            elevation = data[0,0]
            logging.debug("utmEastings:{utmEastings} utmNorthings:{utmNorthings} xOffset:{xOffset} yOffset:{yOffset} band:{bandIndex} elevation:{elevation}".format(**locals()))
            found = True
            break
        else:
            logging.debug("Not present in this file")

    return found, elevation

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, reloader=True, debug=True)

