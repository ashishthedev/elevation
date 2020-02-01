#!/bin/bash

echo '*********************'
echo '***** ubuntu.sh *****'
echo '*********************'

set -euxo pipefail

echo '*** Setup Ubuntu box'

echo ' ** Running apt-get update to be cutting-edge'
sudo apt-get update

echo ' ** Installing core stuff'
sudo apt-get install -y unzip git-core build-essential libxml2-dev libxslt-dev python-dev python-pip tree htop
sudo apt-get install -y python-dev python-pip

echo ' ** Fixing colors'
sed -i 's/#force_color_prompt=yes/force_color_prompt=yes/g' /home/vagrant/.bashrc

echo '*** /Finished setting up Ubuntu box'


if [ -e "/vagrant" ]; then


setup_atd_no_prompt_installer(){

git config --global user.email "ashishthedev@gmail.com"
git config --global user.name "Ashish Anand"
#Only available in vagrant. For staging or production you still need to install keys manually.
mkdir -p /home/vagrant/.ssh

cat << EOL > /home/vagrant/.ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5FXoclw/P2GtmzbhoJ5IFBgl7ut0omF4F5YSR9MWFC/6BdVQIP5SNAaB4zF2cUB2CGkwcpbWRJQayudUmsVtWHJ30+FGy75nYXvuYu5XSzsOzXxqJGkXRKW+L72hxeLtk+VIw/cfpyFyj5ulGNExICUmWDGOWW2YxhDWxbPPiNA1tS7nHXvmsNIDEpJ80YExrZUvX7YVJ6TeOAQJLn53pcTtds4+n2wD9Bt9r2zZWyOVPfRZIZyEcjpYz2eM8jBuJCvDyhSmoW49CDsiMpbVCF2jbB3nEK8YvC+IINa+DXc64oJMihksAyGrmKGe8UYT50wmU1ir7TezWqV4L/kvB atd@Ashishs-MacBook-Pro.local
EOL

cat << EOL > /home/vagrant/.ssh/id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAuRV6HJcPz9hrZs24aCeSBQYJe7rdKJheBeWEkfTFhQv+gXVU
CD+UjQGgeMxdnFAdghpMHKW1kSUGsrnVJrFbVhyd9PhRsu+Z2F77mLuV0s7Ds18a
iRpF0Slvi+9ocXi7ZPlSMP3H6chco+bpRjRMSAlJlgxjlltmMYQ1sWzz4jQNbUu5
x175rDSAxKSfNGBMa2VL1+2FSek3jgECS5+d6XE7XbOPp9sA/Qbfa9s2VsjlT30W
SGchHI6WM9njPIwbiQrw8oUpqFuPQg7IjKW1Qhdo2wd5xCvGLwviCDWvg13OuKCT
IoZLAMhq5ihnvFGE+dMJlNYq+03s1qleC/5LwQIDAQABAoIBAQCDFvUgXtYyLmUT
sU2VZ8GCkV4SJq4R3Klrn76f6jAkJfSjGMjl9rJulOJl7Mm4tv3PcnTKLYxGO2Vd
HUYdW60HdsliAqdLB2191Ph6mxJo902hNBEFXnhoxuJcyLq+8/Y2dGiEjpsTuHf1
Fs3OjaghtYJLJoc6rY3aMHwfKL4sTeGBJyr5oHeNurU6YoY//q8PDfVHv38GIEnT
Wf0J1ReCejfqHBbL5Bx5AmnagzM/cPGWx3KtZat6S8rlBSw9sbvDT6UIC0KFKqAX
GMfrgbw43ZXmTPGByalBKMGmNy2deIf9N275qEKkcqixWPwZQFMnkN8KCKVOWpwP
VaOrkUTJAoGBANtrHzZPKO3R+bol7dDORsnkMjhLjrtswueI9iErolpCL7Pq+0yX
FIto496+njalMSKirm2HVDcsSQ253aIXKoNSp54J/JoTOoZMq9oj1YRTNNp7XR31
OqaihFCE2/tXSBtAAOr2FE9n8slFAnJdSIgXhvkpGVeKNDVTAQmD7q5nAoGBANfw
8OUELSvnt9S+X0RdLp2p8zh9dtSClZ5ehUHiBVpgwJ3v2Ky8KFQKaKGt8w27TF/V
vBC1jnKA8qJyuiS9C/Kyz9vzBYTZCSL69oKCqK61Df/5caRzAn10oIZ6PvTcW47t
9ILf3eO+7PcJTBfLkeofSHFh462O/iZsXQhRMQuXAoGAUhD+25E//bNLdBQ7np2I
XHq9TdD00aUcQP05Ea8ASkH3FZQN6deYF4xjriwdgNLITewK0WyMUxZ9PGUIQFfp
zrRbfQC/OeF3QkPrAuvkMFnuqsj5SvsttKWUV4lZvegnUAngTgE8F3cJl7337E53
km86THbSw6stW8Rv3t85poECgYEAg4Vwc0wz5wXe5Wh9xbmrZsPYK5PfCFfwoOCY
8SOkdwNuzcMDiVGgjm84gyDbZIWrYsNfJB4wgHUhUuflj/LEkDFwgFpoBh3afr+z
3JGQA7iqqjlXif2yio66Jq3WInUEHu23eu62yrvCwEOdYPDQEnSzPruMXG03RlfB
4grxgEkCgYEAoExpdYUUmhUwgw0CSSkYj3R/baBmDe76uqFgeAu/PGTxps0qGNPa
8xDx+p1Z91vcIpZpRqihhwvnU+xmnoo0jD1Hx2C/VHtnnXUm2SbDUClNVxoo1vPy
a4y7M5U9ytDa8FXNoHhKQsWaw4ZuBgQxIDtr8TQoqBpamJ8WpErUdWM=
-----END RSA PRIVATE KEY-----
EOL

cat /home/vagrant/.ssh/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
chmod -R go= /home/vagrant/.ssh
chown -R vagrant:vagrant /home/vagrant/.ssh
eval "$(ssh-agent -s)"
ssh-add /home/vagrant/.ssh/id_rsa
}

#call
setup_atd_no_prompt_installer

fi

