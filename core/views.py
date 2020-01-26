############################################
## Elevation as a service.
## Author: Ashish Anand
## Date: 2020-01-26
############################################


from django.shortcuts import render
from django.http import JsonResponse
import subprocess


def index(request):
	return render(request, 'core/home.html')


def ping(request):
	return JsonResponse({"status": "ok"})


def elevation(request, lat, lng):
	print("Got lat: {}, lng: {}".format(lat, lng))
	cmd = ["python", "elevation_prog.py", "--lat", lat, "--lng", lng]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	stdout, stderr = proc.communicate()
	if stdout:
 		return JsonResponse({
 			"elevation": str(stdout.rstrip().decode("utf-8") )
        })
	elif stderr:
 		return JsonResponse({
 			"elevation": str(stderr)
        })
	else:
		return JsonResponse({
 			"elevation": "NA"
        })



