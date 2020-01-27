from django.db import models

# Create your models here.

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
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(blank=True, null=True)
    time_taken = models.DurationField(blank=True, null=True)
    log_text = models.TextField(blank=True, null=True)

    def __str__(self):
    	return f"{self.name} {self.state}"

    @classmethod
    def _getCurrentStateFor(cls, zoneName):
        return cls.objects.get_or_create(name=zoneName).state

    @classmethod
    def provision(cls, zoneName):

        state = cls._getCurrentStateFor(zoneName)
        if state == SUCCESS:
            raise ProvisioningException(f"{zoneName} is already provisioned.")
        elif state == WIP:
            raise ProvisioningException(f"{zoneName} is currently in projress.")
        elif state == INITIAL or state == FAILURE:
            cls._provision(zoneName)
        return

    @classmethod
    def _provision(cls, zoneName):
        if zoneName not in ZIP_FILES:
            raise ProvisioningException(f"{zoneName} is unknown. Code change is required for its provisioning.")
        zip_file_url = ZIP_FILES[zoneName]

        obj = cls.objects.get_or_create(name=zoneName)


        return




