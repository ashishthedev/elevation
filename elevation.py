###########################################################
##                    DYSFUNCTIONAL
###########################################################

###########################################################
## NOT THIS BOTTLE BASED WEBSERVER USING ANYMORE. 
## WE HAVE SWITCHED TO DJANGO SERVER NOW. PLEASE REFER TO
## THAT.
###########################################################


###########################################################
## Bottle server for elevation service
## 2016-Feb-16 Tue 01:57 PM
###########################################################

import bottle
from bottle import run, response
import fnmatch
import gdal
import json
import logging
import os
import time
from provision import provisionZoneName, determineProvisioningCurrentState

logging.basicConfig(filename='elevation.log', format=logging.BASIC_FORMAT, level=logging.DEBUG)
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
    for filename in getGlobbedFiles():
        noDataValue = GetNoDataValueForFile(filename)
        elevation = searchElevationForLatLngInFile(filename, lat, lng)
        if elevation and elevation != noDataValue and elevation not in KNOWN_NO_DATA_VALUES:
            logging.info("{} - Found elevation {} in file {}".format(time.time(), elevation, filename))
            return elevation
    else:
        return "NA"

app = bottle.default_app()
gdal.AllRegister()

@app.route('/')
def index():

    html = """
<html>
<head>
<meta name="author" content="Ashish Anand">
<meta name="email" content="ashishthedev@gmail.com">
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" integrity="sha256-7s5uDGW3AHqw6xtJmNNtr+OBRJUlgkNJEo78P4b0yRw= sha512-nNo+yCHEyn0smMxSswnf/OnX6/KwJuZTlNZBjauKhTK0c+zT+q5JOCx0UFhXQ6rJR9jg6Es8gPuD2uZcYDLqSw==" crossorigin="anonymous">
</head>
<body>
<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="/">Elevation as Service</a>
    </div>
    <ul class="nav navbar-nav">
      <li class="active"><a href="/">Home</a></li>
    </ul>
  </div>
</nav>
    <div class="container">
    <h2>Status:</h2>
    <pre>
    Elevation Service Running</pre>
    <h2>Usage:</h2>
    <pre>
    http://elevation.adaptinfrastructure.com/elevation/lat/-12.659170573364879/lng/132.255024546978</pre>
    <h2>How to add more GIS data on server:</h2>
    <h4>Step 1:</h4>
    <pre>
    cd zippedAdfFiles
    wget https://s3-ap-southeast-2.amazonaws.com/crcsi.ga.gov.au/5m-dem/NSW5mDEM.zip</pre>
    <h4>Step 2:</h4>
    <pre>
    cd unzippedAdfFiles
    mkdir NSW5mDEM
    cd NSW5mDEM
    7za e ../../zippedAdfFiles/NSW5mDEM.zip
    sudo restart elevation</pre>
    </div>
</body>
"""
    return html


@app.route('/elevation/ping')
@enable_cors
def ping():
    from json import dumps
    rv = "ok"
    response.content_type = 'application/json'
    return dumps(rv)


@app.route('/elevation/lat/<lat>/lng/<lng>')
@enable_cors
def elevation(lat, lng):
    response.content_type = 'application/json'
    return json.dumps({
        "elevation": searchElevationForLatLng(lat, lng)
        })


@app.route('/provisioningCurrentState/<zoneName>')
@enable_cors
def provisioningCurrentState(zoneName):
    response.content_type = 'application/json'
    return json.dumps(determineProvisioningCurrentState(zoneName))


@app.route('/startProvisioning/<zoneName>')
@enable_cors
def startProvisioning(zoneName):
    provisionZoneName(zoneName)
    response.content_type = 'application/json'
    return json.dumps({"status_msg": "Provisioning of {} is complete.".format(zoneName)})


if __name__ == "__main__":
    run(host='0.0.0.0', port=8282, reloader=True, debug=True)

