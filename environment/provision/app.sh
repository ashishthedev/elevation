#!/bin/bash

echo '*********************'
echo '******* app.sh ******'
echo '*********************'

set -euxo pipefail

install_gdal(){
		sudo apt-get -y install libgdal-dev	
		# sudo pip install GDAL	
		export CPLUS_INCLUDE_PATH=/usr/include/gdal
		export C_INCLUDE_PATH=/usr/include/gdal
		sudo apt-get -y install python-gdal
		sudo apt-get install gdal-bin
	}


#Once the app has been cloned, you can use this file to add custom requirements
#for ex
#pip install -r requirements.txt -t lib/
sudo apt-get -y install gunicorn git p7zip-full nginx python-pip htop tree
git config credential.helper store
sudo apt-get install -y python3 python3-pip python3-venv
sudo -H pip3 install --upgrade pip
sudo pip3 install -r requirements.txt

install_gdal

echo ' ****** Adding locale settings to .bash_profile'
sudo cat << EOT >> /home/vagrant/.bash_profile
# Set locales in /etc/default/locale file
# Locale settings
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
sudo locale-gen en_US.UTF-8
#sudo dpkg-reconfigure locales
EOT


if [ -e "/vagrant/app/package.json" ]; then
	cd /vagrant/app && npm install
fi

