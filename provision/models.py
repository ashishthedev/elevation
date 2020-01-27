#################################################################
## Elevation on demand provisioners
## Ashish Anand
#################################################################

from django.db import models
from subprocess_logging import subprocess_call_with_output_returned
import datetime

ZIP_FILES = {
	"NT5": "https://storage.googleapis.com/elevation_rawdata_zipped_bucket/NT5mDEM.zip",
	"NSW": "https://storage.googleapis.com/elevation_rawdata_zipped_bucket/NSW5mDEM.zip",
	"QLD": "https://storage.googleapis.com/elevation_rawdata_zipped_bucket/QLD5mDEM.zip",
	"SA" : "https://storage.googleapis.com/elevation_rawdata_zipped_bucket/SA5mDEM.zip",
	"TAS": "https://storage.googleapis.com/elevation_rawdata_zipped_bucket/TAS5mDEM.zip",
	"VIC": "https://storage.googleapis.com/elevation_rawdata_zipped_bucket/VIC5mDEM.zip",
	"WA" : "https://storage.googleapis.com/elevation_rawdata_zipped_bucket/WA5mDEM.zip",

}
INITIAL = "INITIAL"
SUCCESS = "SUCCESS"
FAILURE = "FAILURE"
WIP = "WIP"
STATE_CHOICES = (
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE),
        (WIP, WIP),
        (INITIAL, INITIAL),
    )

class ProvisioningException(Exception):
    pass

class Provisioner(models.Model):
    zoneName = models.CharField(max_length=10)
    state = models.CharField(blank=True, choices=STATE_CHOICES, max_length=10, default=INITIAL)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    time_taken = models.DurationField(blank=True, null=True)
    log_text = models.TextField(blank=True, null=True)

    def __str__(self):
    	return f"{self.zoneName} {self.state}"

    @classmethod
    def getCurrentStateFor(cls, zoneName):
        obj, _ = cls.objects.get_or_create(zoneName=zoneName)
        return obj.state

    @classmethod
    def provision(cls, zoneName):

        state = cls.getCurrentStateFor(zoneName)
        if state == SUCCESS:
            raise ProvisioningException(f"{zoneName} is already provisioned.")
        elif state == WIP:
            raise ProvisioningException(f"{zoneName} is currently in projress.")
        elif state == INITIAL or state == FAILURE:
            cls._provision(zoneName)
        return

    @classmethod
    def _provision(cls, zoneName):
        obj, _ = cls.objects.get_or_create(zoneName=zoneName)
        if obj.state not in [INITIAL, FAILURE]:
            raise Exception("We should not have reached here.")
        obj.log_text = ""
        obj.state = WIP
        obj.started_at = datetime.datetime.now()

        obj.save()
        try:
            if zoneName not in ZIP_FILES:
                raise ProvisioningException(f"{zoneName} is unknown. If this is a new zone, then code change is required for its provisioning.")

            zip_file_url = ZIP_FILES[zoneName]
            outs, errs = subprocess_call_with_output_returned("ls")
            import time; time.sleep(10)
            # with cd(UNZIPPED_FILES_DIR):
            # subprocess_call_with_logging(
            #     logFileForZone(zoneName),
            #     ["7za", "e", os.path.join(ZIPPED_FILES_DIR, zoneName + ".zip")]
            #     )

            obj.log_text = outs or errs
            if outs:
                obj.state = SUCCESS
            elif errs:
                obj.state = FAILURE
        except Exception as ex:
            obj.log_text = str(ex)
            obj.state = FAILURE
        finally:
            obj.finished_at = datetime.datetime.now()
            obj.time_taken = obj.finished_at - obj.started_at
            obj.save()
        return




