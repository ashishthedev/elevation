############################################
## Elevation as a service.
## Author: Ashish Anand
## Date: 2020-01-26
############################################


import logging

from django.shortcuts import render
from django.http import JsonResponse
from core.misc import searchElevationForLatLng

logging.basicConfig(filename='elevation.log', format=logging.BASIC_FORMAT, level=logging.DEBUG)
logging.info('_'*70)


def index(request):
	return render(request, 'core/home.html')

def ping(request):
	return JsonResponse({"status": "ok"})



def elevation(request, lat, lng):
	logging.info("Got lat: {}, lng: {}".format(lat, lng))
	return JsonResponse({
        "elevation": "20",
        # "elevation": searchElevationForLatLng(lat, lng)
        })

