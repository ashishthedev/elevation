#!/bin/bash

echo '*********************'
echo '**** dotfiles.sh ****'
echo '*********************'

set -euxo pipefail

echo '*** Setup dotfiles'

echo ' ** Cloning repo'
git clone https://bitbucket.org/ashishthedev/vagrant_dotfiles/ -b master /home/vagrant/vagrant_dotfiles
cd vagrant_dotfiles
sudo chmod a+x setup.sh
echo ' ** Executing setup.sh'
sudo su vagrant -c "/home/vagrant/vagrant_dotfiles/setup.sh /home/vagrant"

#vagrant_dotfiles contains aliases. Create a soft link from that aliases.
sudo su vagrant -c "ln -sf /vagrant/environment/utils/custom.aliases.bash /home/vagrant/.bash_it/aliases/custom.aliases.bash"

