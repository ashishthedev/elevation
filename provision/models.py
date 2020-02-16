#################################################################
## Elevation on demand provisioners
## Ashish Anand
#################################################################

from django.db import models
from subprocess_logging import subprocess_call_with_output_returned
import datetime
import os
import textwrap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIPPED_FILES_DIR = os.path.join(BASE_DIR, "rawData", "zippedAdfFiles")
UNZIPPED_FILES_DIR = os.path.join(BASE_DIR, "rawData", "unzippedAdfFiles")


ZIP_FILES = {
	"NT5": "gs://elevation_rawdata_zipped_bucket/NT5mDEM.zip",
	"NSW": "gs://elevation_rawdata_zipped_bucket/NSW5mDEM.zip",
	"QLD": "gs://elevation_rawdata_zipped_bucket/QLD5mDEM.zip",
	"SA" : "gs://elevation_rawdata_zipped_bucket/SA5mDEM.zip",
	"TAS": "gs://elevation_rawdata_zipped_bucket/TAS5mDEM.zip",
	"VIC": "gs://elevation_rawdata_zipped_bucket/VIC5mDEM.zip",
	"WA" : "gs://elevation_rawdata_zipped_bucket/WA5mDEM.zip",

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
    	return "{}".format(self.zoneName, self.state)

    @classmethod
    def getCurrentStateFor(cls, zoneName):
        obj, _ = cls.objects.get_or_create(zoneName=zoneName)
        return obj.state

    @classmethod
    def provision(cls, zoneName):

        state = cls.getCurrentStateFor(zoneName)
        if state == SUCCESS:
            raise ProvisioningException("{zoneName} is already provisioned.".format(zoneName=zoneName))
        elif state == WIP:
            raise ProvisioningException("{zoneName} is currently in projress.".format(zoneName=zoneName))
        elif state == INITIAL or state == FAILURE:
            cls._provision(zoneName)
        return

    @classmethod
    def _provision(cls, zoneName):
        obj, _ = cls.objects.get_or_create(zoneName=zoneName)
        if obj.state not in [INITIAL, FAILURE]:
            raise ProvisioningException("We should not have reached here.")
        obj.log_text = ""
        obj.state = WIP
        obj.started_at = datetime.datetime.now()
        obj.finished_at = None
        obj.time_taken = None
        obj.save()
        try:
            if zoneName not in ZIP_FILES:
                raise ProvisioningException("{zoneName} is unknown. If this is a new zone, then code change is required for its provisioning.".format(zoneName=zoneName))

            cmd = "python3 provision_prog.py --zoneName {zoneName}".format(zoneName=zoneName)
            obj.log_text = "Cmd: {cmd}".format(cmd=cmd)

            outs, errs = subprocess_call_with_output_returned(cmd, shell=True)

            if outs:
                outs = outs.decode("utf-8")
                obj.log_text += "\nSUCCESS_MSG: {outs}".format(outs=outs)
                obj.state = SUCCESS
            elif errs:
                errs = errs.decode("utf-8")
                obj.log_text += "\nERROR_MSG: {errs}".format(errs=errs)
                obj.state = FAILURE
        except Exception as ex:
            if cmd:
                obj.log_text += "\n{cmd} Exception: {ex}".format(cmd=cmd, ex=ex)
            else:
                obj.log_text += "\nException: {ex}".format(ex=ex)
            obj.state = FAILURE
        finally:
            obj.finished_at = datetime.datetime.now()
            obj.time_taken = obj.finished_at - obj.started_at
            obj.save()
        return




