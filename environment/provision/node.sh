#!/bin/bash

echo '*********************'
echo '***** node.sh *******'
echo '*********************'

set -euxo pipefail

sudo mkdir /vagrant_node_modules
chown vagrant:vagrant /vagrant_node_modules

if [ ! -e "/vagrant/node_modules" ]; then
	sudo mkdir /vagrant/node_modules
fi
sudo mount --bind /vagrant_node_modules /vagrant/node_modules

sudo apt-get install curl
curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
sudo apt-get install -y nodejs


if [ -e "/vagrant/package.json" ]; then
	cd /vagrant/ && npm install -f
fi