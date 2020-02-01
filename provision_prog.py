import os
import logging
import argparse
import textwrap
import subprocess
import sys

logging.basicConfig(filename='provision_prog.log', format=logging.BASIC_FORMAT, level=logging.DEBUG)
logging.info('_'*70)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UNZIPPED_FILES_DIR = os.path.join(BASE_DIR, "rawData", "unzippedAdfFiles")
ZIPPED_FILES_DIR = os.path.join(BASE_DIR, "rawData", "zippedAdfFiles")
FILE_FORMAT = "hdr.adf"

KNOWN_NO_DATA_VALUES = [
        #Sometimes, we are unable to pythonically read no data values, but the binary utility still reports the correct no data value. For those cases, known no data values can be supplied here.
"-3.40282346638529e+38",
]


ZIP_FILES = {
    "NT5": "gs://elevation_rawdata_zipped_bucket/NT5mDEM.zip",
    "NSW": "gs://elevation_rawdata_zipped_bucket/NSW5mDEM.zip",
    "QLD": "gs://elevation_rawdata_zipped_bucket/QLD5mDEM.zip",
    "SA" : "gs://elevation_rawdata_zipped_bucket/SA5mDEM.zip",
    "TAS": "gs://elevation_rawdata_zipped_bucket/TAS5mDEM.zip",
    "VIC": "gs://elevation_rawdata_zipped_bucket/VIC5mDEM.zip",
    "WA" : "gs://elevation_rawdata_zipped_bucket/WA5mDEM.zip",

}


def subprocess_call_with_output_returned(popenargs, **kwargs):
    proc = subprocess.Popen(popenargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    outs, errs = proc.communicate()
    return outs, errs

def provisionZone(zoneName):
    source_zip_file_url = ZIP_FILES[zoneName]
    dest_zip_file_path = os.path.join(ZIPPED_FILES_DIR, os.path.basename(source_zip_file_url))
    cmd = textwrap.dedent(f"""mkdir -p {ZIPPED_FILES_DIR} && \
            sudo gsutil cp {source_zip_file_url} {dest_zip_file_path} && \
            mkdir -p {UNZIPPED_FILES_DIR} && \
            cd {UNZIPPED_FILES_DIR} && \
            mkdir {zoneName} && \
            cd {zoneName} && \
            sudo 7za e {dest_zip_file_path}
            """)
    outs, errs = subprocess_call_with_output_returned(cmd, shell=True)
    return outs, errs


if __name__ == "__main__":
    # python3 provision_prog.py --zoneName NT5
    parser = argparse.ArgumentParser(description='Provision zones for elevation service.')
    parser.add_argument('--zoneName', dest='zoneName', type=str, help='zoneName')

    args = parser.parse_args()
 
    outs, errs = provisionZone(args.zoneName)
    if outs:
        print(outs.decode("utf-8"))
        exit(0)
    elif errs:
        print(errs.decode("utf-8"), file=sys.stderr)
        exit(1)
    else:
        print("No output from provisionZone()", file=sys.stderr)
        exit(1)
