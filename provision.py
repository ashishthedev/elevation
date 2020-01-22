###########################################################
## Zipping, Unzipping, WIP-detection for Provisioners in 
## Elevation Terraform project
## Author: Ashish Anand
###########################################################
import os

from file_logging import subprocess_call_with_logging

ZIPPED_FILES_DIR = "/var/elevation/rawData/zippedAdfFiles"
UNZIPPED_FILES_DIR = "/var/elevation/rawData/unzippedAdfFiles"
WIP_DIR = "/var/elevation/rawData/wip"


##############################
## FILE OPERATIONS
##############################

def touch(filepath):
    with open(filepath, 'a'):
        os.utime(filepath, None)
    return

def ensureDirExists(dirpath):
	os.makedirs(dirpath, exist_ok=True)
	return

def silentremove2(filename):
    import errno
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def silentremove(filename):
    if os.path.exists(filename):
        os.remove(filename)

##############################
## SUCCESS INDICATORS
##############################

def successFilePath(zoneName):
	return os.path.join(WIP_DIR, zoneName + ".success")

def decalareSuccessForZone(zoneName):
	touch(successFilePath(zoneName))

def isSuccessIndicatorPresent(zoneName):
	return os.path.exists(successFilePath(zoneName))


##############################
## FAILURE INDICATORS
##############################

def failFilePath(zoneName):
	return os.path.join(WIP_DIR, zoneName + ".fail")

def decalareFailureForZone(zoneName):
	touch(failFilePath(zoneName))

def isFaliureIndicatorPresent(zoneName):
	return os.path.exists(failFilePath(zoneName))


##############################
## CLEANUP / FRESH START
##############################

def cleanupIndicatorsForZone(zoneName):
	silentremove(successFilePath(zoneName))
	silentremove(failFilePath(zoneName))
	silentremove(logFileForZone(zoneName))
	silentremove(wipFileForZone(zoneName))
	return


#########
## WIP
#########

def wipFileForZone(zoneName):
	return os.path.join(WIP_DIR, zoneName + ".wip")

def setWIPFile(zoneName):
	wipFilePath = wipFileForZone(zoneName)
	ensureDirExists(WIP_DIR)
	touch(wipFilePath)
	return

def deleteWIPFile(zoneName):
	wipFilePath = wipFileForZone(zoneName)
	if os.path.exists(wipFilePath):
		os.remove(wipFilePath)
	return

def isWIPFilePresent(zoneName):
	wipFilePath = os.path.join(WIP_DIR, zoneName)
	return os.path.exists(wipFilePath)


#########
## LOG
#########

def logFileForZone(zoneName):
	return os.path.join(WIP_DIR, zoneName + ".log")

def setLogFile(zoneName):
	logFilePath = logFileForZone(zoneName)
	ensureDirExists(WIP_DIR)
	touch(logFilePath)
	return

def deleteLogFile(zoneName):
	logFilePath = logFileForZone(zoneName)
	if os.path.exists(logFilePath):
		os.remove(logFilePath)
	return

def isLogFilePresent(zoneName):
	logFilePath = logFileForZone(zoneName)
	return os.path.exists(logFilePath)

def logFileContentsForZone(zoneName):
	logFilePath = logFileForZone(zoneName)
	if os.path.exists(logFilePath):
		with open(logFileForZone(zoneName), "r") as f:
			return f.read()
	return ""

def provisionZoneName(zoneName):
	if isWIPFilePresent(zoneName): return
	ensureDirExists(UNZIPPED_FILES_DIR)
	ensureDirExists(WIP_DIR)

	try:
		cleanupIndicatorsForZone(zoneName)
		setWIPFile(zoneName)
		with cd(UNZIPPED_FILES_DIR):
			subprocess_call_with_logging(
				logFileForZone(zoneName),
				["7za", "e", os.path.join(ZIPPED_FILES_DIR, zoneName + ".zip")]
				)
		decalareSuccessForZone(zoneName)
	finally:
		decalareFailureForZone(zoneName)
		deleteWIPFile(zoneName)
	return

def determineProvisioningCurrentState(zoneName):
	stateDict = {
		"IN_PROGRESS": isWIPFilePresent(zoneName),
		"SUCCESS": isSuccessIndicatorPresent(zoneName),
		"FAILURE": isFaliureIndicatorPresent(zoneName),
		"LOG": logFileContentsForZone(zoneName)
	}
	return stateDict


#########
## CD
#########

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

# 	unzip_adf_files(){
# 		set +x
# 		echo "======================================"
# 		echo "Unzipping all adf Files"
# 		echo "======================================"
# 		set -x 
# 		mkdir -p /var/elevation/rawData/unzippedAdfFiles
# 		cd /var/elevation/rawData/unzippedAdfFiles
# 		FILES=/var/elevation/rawData/zippedAdfFiles/*.zip
# 		for f in $FILES
# 		do
# 			set +x
# 			echo "======================================"
# 			echo "Unzipping adf File: "
# 			echo $f
# 			echo "======================================"
# 			set -x 
# 			dirname=$(basename $f .zip)
# 			mkdir $dirname
# 			cd $dirname
# 			7za e $f
# 			cd ..
# 		done

# 	}