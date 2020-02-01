#!/bin/bash

#Inspiration
#https://raw.githubusercontent.com/laander/vagrant-gcloud/master/environment/provision/gcloud.sh
echo '*********************'
echo '***** gcloud.sh *****'
echo '*********************'

set -euxo pipefail

echo '*** Setup Google Cloud SDK'

echo ' ** Installing python packages'
sudo apt-get install -y python-dev python-setuptools python-pip  python g++ make
# sudo apt-get install -y python-software-properties #For ubuntu 16
sudo apt-get install -y software-properties-common   # For ubuntu 18

# Make the helper binaries executable and globally available
echo ' ** Setup support CLI commands'
echo 'export PATH=/vagrant/environment/utils:$PATH' >> /home/vagrant/.bash_profile
cd /vagrant/environment/utils
chmod +x app-server
chmod +x app-deploy

# Download Cloud SDK
echo ' ** Setup Google Cloud SDK command-line tools'
echo '  * Downloading Cloud SDK'
cd /home/vagrant
wget -q https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz
tar xzvpf google-cloud-sdk.tar.gz
rm google-cloud-sdk.tar.gz

# Silent install Cloud SDK
echo '  * Installing Cloud SDK'
./google-cloud-sdk/install.sh --rc-path=/home/vagrant/.bash_profile --bash-completion=true --path-update=true --disable-installation-options

# Install GAE language packages
echo '  * Installing Cloud SDK python deps'
./google-cloud-sdk/bin/gcloud components update app-engine-go app-engine-python app-engine-python-extras --quiet

sudo chown vagrant:vagrant -R google-cloud-sdk/

echo '*** /Finished setting up Cloud SDK'
