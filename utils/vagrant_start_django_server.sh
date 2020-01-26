#!/bin/bash

if [ ! -e '/vagrant' ] ; then
	echo "This should only be run from inside vagrant environment."
	exit 1
fi
echo "***************************************"
echo "App running on http://localhost:9092"
echo "***************************************"
cd /vagrant && python3 manage.py runserver 0.0.0.0:9092