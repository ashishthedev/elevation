#!/bin/bash

echo '**********************************'
echo '*** golang-go-discontinued.sh ****'
echo '**********************************'

set -euxo pipefail

sudo apt-get install golang-go -y


# Write environment variables, other prompt and automatic cd into /vagrant in the bashrc
echo "Editing .bashrc ..."
HOMEPATH="/home/vagrant"

cat << EOT >> $HOMEPATH/.bashrc
export GOPATH=$HOMEPATH/.go
export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
EOT

export PATH=$PATH:/usr/local/go/bin
export GOPATH=/home/vagrant/.go
