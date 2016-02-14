#!/bin/bash

cd /home/ashishthedev/elevation/
exec gunicorn -c deploy/gunicorn.conf.py elevation:app
