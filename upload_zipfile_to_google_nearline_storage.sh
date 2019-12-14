#!/bin/bash

# Usage: upload_to_google_nearline_storage.sh /path/to/foobar.zip

gsutil cp $1 gs://elevation_rawdata_zipped_bucket/
