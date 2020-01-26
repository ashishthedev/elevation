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
SUCCESS = "SUCCESS"
FAILURE = "FAILURE"
WIP = "WIP"
STATE_CHOICES = (
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE),
        (WIP, WIP),
    )
class Provisioner(models.Model):
    name = models.CharField(max_length=10)
    state = models.CharField(blank=True, choices=STATE_CHOICES, max_length=10)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(blank=True, null=True)
    time_taken = models.DurationField(blank=True, null=True)

    def __str__(self):
    	return f"{self.name} {self.state}"
