#!/bin/sh
set +x
GUNICORN="/usr/local/bin/gunicorn"
PROJECTLOC="/var/elevation"
cd /var/elevation && gunicorn -c /var/elevation/deploy/gunicorn.conf.py elevation.wsgi --daemon
