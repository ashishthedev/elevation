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
	cmd = ["python", "elevation_prog.py", "--lat", lat, "--lng", lng]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	stdout, stderr = proc.communicate()
	if stdout:
		if (len(stdout.split()) == 1):
	 		return JsonResponse({
	 			"status": "success",
	 			"elevation": str(stdout.rstrip().decode("utf-8") )
	        })
		else:
	 		return JsonResponse({
	 			"status": "failure",
	 			"elevation": str(stdout.rstrip().decode("utf-8") )
	        })
	elif stderr:
 		return JsonResponse({
 			"status": "failure",
 			"elevation": str(stderr.rstrip().decode("utf-8") )
        })
	else:
		return JsonResponse({
 			"status": "failure",
 			"elevation": "NA"
        })

