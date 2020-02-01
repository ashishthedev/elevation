#!/bin/bash

echo '************************'
echo '***** golang-go.sh *****'
echo '************************'

set -euxo pipefail

# Golang installation variables
VERSION="1.9"
OS="linux"
ARCH="amd64"

# Home of the vagrant user, not the root which calls this script
HOMEPATH="/home/vagrant"

# Updating and installing stuff
sudo apt-get update
sudo apt-get install -y git curl

if [ ! -e "/vagrant/go.tar.gz" ]; then
	# No given go binary
	# Download golang
	FILE="go$VERSION.$OS-$ARCH.tar.gz"
	URL="https://storage.googleapis.com/golang/$FILE"

	echo "Downloading $FILE ..."
	curl --silent $URL -o "$HOMEPATH/go.tar.gz"
else
	# Go binary given
	echo "Using given binary ..."
	cp "/vagrant/go.tar.gz" "$HOMEPATH/go.tar.gz"
fi;

echo "Extracting ..."
tar -C "$HOMEPATH" -xzf "$HOMEPATH/go.tar.gz"
mv "$HOMEPATH/go" "$HOMEPATH/.go"
rm "$HOMEPATH/go.tar.gz"

# Create go folder structure
GP="/vagrant/gopath"
mkdir -p "$GP/src"
mkdir -p "$GP/pkg"
mkdir -p "$GP/bin"

# Write environment variables, other prompt and automatic cd into /vagrant in the bashrc
echo "Editing .bashrc ..."
cat << EOT >> $HOMEPATH/.bashrc
# Golang environments
export GOROOT=$HOMEPATH/.go
export GOPATH=$GP
export PATH=\$PATH:\$GOROOT/bin:\$GOPATH/bin
EOT

# https://github.com/fatih/vim-go
# You will also need to install all the necessary binaries. vim-go makes it easy to install all of them by providing a command, :GoInstallBinaries, which will go get all the required binaries.
git clone https://github.com/fatih/vim-go.git ~/.vim/bundle/vim-go #TODO: Test it
