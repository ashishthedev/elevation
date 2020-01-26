#!/bin/bash

echo '***********************'
echo '******* django.sh *****'
echo '***********************'

set -euxo pipefail

sudo apt-get -y update

sudo apt-get install -y python3 python3-pip python3-dev nginx

sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv

# sudo -H pip3 install Django==2.0.7 #Will be in requirements.txt which will be invoked from app.sh
touch .gitignore
cat >> .gitignore<<EOL
.env
.*py?
EOL

echo '********************************'
echo 'Follow the instructions now to setup Django project.'
echo 'https://www.digitalocean.com/community/tutorials/how-to-install-the-django-web-framework-on-ubuntu-16-04'
echo '********************************'

echo "
mkdir ~/myproject
cd ~/myproject

virtualenv myprojectenv

source myprojectenv/bin/activate


source myprojectenv/bin/activate

pip install django

nano myproject/settings.py

ALLOWED_HOSTS = ['server_domain_or_IP']

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

cd ~/myproject
./manage.py makemigrations
./manage.py migrate

./manage.py createsuperuser

./manage.py collectstatic

sudo ufw allow 8000

./manage.py runserver 0.0.0.0:8000
http://server_domain_or_IP:8000

deactivate



chmod 664 ~/myproject/db.sqlite3

sudo chown :www-data ~/myproject/db.sqlite3

sudo chown :www-data ~/myproject

sudo ufw delete allow 8000

sudo ufw allow 'Nginx Full'

"



