from django.http import JsonResponse


def startProvisioning(request):
	return JsonResponse({"status": "ok"})

def provisioningCurrentState(request):
	return JsonResponse({"status": "ok"})