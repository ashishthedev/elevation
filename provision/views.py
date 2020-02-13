from django.http import JsonResponse
from provision.models import Provisioner
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def startProvisioning(request, zoneName):
	Provisioner.provision(zoneName)
	return provisioningCurrentState(request, zoneName)


# POSSIBLE STATES
# (SUCCESS, SUCCESS),
# (FAILURE, FAILURE),
# (WIP, WIP),
# (INITIAL, INITIAL),

def provisioningCurrentState(request, zoneName):
	current_state = Provisioner.getCurrentStateFor(zoneName)
	if current_state == "SUCCESS":
		return JsonResponse({
			"state": current_state,
			"status_msg": "Provisioned successfully",
			"wip": False,
			"isProvisioned": True,
			})
	elif current_state == "FAILURE":
		return JsonResponse({
			"state": current_state,
			"status_msg": "Failed",
			"wip": False,
			"isProvisioned": False,
			})
	elif current_state == "WIP":
		return JsonResponse({
			"state": current_state,
			"status_msg": "Initializing...",
			"wip": True,
			"isProvisioned": False,
			})
	elif current_state == "INITIAL":
		return JsonResponse({
			"state": current_state,
			"status_msg": "Not initialized...",
			"wip": False,
			"isProvisioned": False,
			})
