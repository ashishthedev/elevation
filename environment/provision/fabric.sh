echo ' ** Installing core stuff'
sudo apt-get install -y unzip git-core build-essential libxml2-dev libxslt-dev  tree htop
sudo apt-get install -y python3-dev python3-pip
sudo apt-get install -y python-dev python-pip

# pip3 install --upgrade pip3

# echo '*** Installing fabric==1.12.1'
# sudo pip2 install fabric==1.12.1

echo '*** Installing fabric3'
sudo pip3 install fabric3