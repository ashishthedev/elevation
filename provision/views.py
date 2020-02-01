from django.http import JsonResponse
from provision.models import Provisioner

def startProvisioning(request, zoneName):
	Provisioner.provision(zoneName)
	return JsonResponse({"status": "WIP"})

def provisioningCurrentState(request, zoneName):
	Provisioner.getCurrentStateFor(zoneName)
	return JsonResponse({"status": "ok"})