#!/bin/bash

cd /var/elevation/
sudo bash -c "gunicorn -c deploy/gunicorn.conf.py elevation:app"
