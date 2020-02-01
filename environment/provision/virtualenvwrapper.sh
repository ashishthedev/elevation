sudo pip3 install virtualenvwrapper

sudo cat << EOT >> /home/vagrant/.bashrc

export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
EOT

