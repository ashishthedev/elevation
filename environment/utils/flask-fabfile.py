#Currently meant for django. Need to implement for flask


#Inspired by: https://samoylov.eu/2016/09/29/deploying-django-with-fabric/

"""
Usage: 
fab staging bootstrap
fab staging deploy

fab vagrant bootstrap 
fab vagrant deploy

fab production bootstrap
fab production deploy
"""

import os  
from contextlib import contextmanager  
from fabric.api import cd, env, prefix, run, sudo, task
from fabric.network import ssh

PROJECT_NAME = 'emailer'
REPO = 'git@bitbucket.org:ashishthedev/{}.git'.format(PROJECT_NAME)

HOME = '/home/ashish_the_dev'
PROJECT_ROOT = '{home}/wk/{project_name}'.format(home=HOME, project_name=PROJECT_NAME)  
VENV_DIR = os.path.join(HOME, '.virtualenvs')  
env.user="ashish_the_dev"

env.hosts = []

ssh.util.log_to_file("paramiko.log", 10)

@task
def vagrant():  
    env.hosts = ['localhost:22']#copy your id_rsa and id_rsa.pub in vagrant's ssh folder and add id_rsa.pub to authorized_keys
    env.user="vagrant"
    env.environment = 'production'
    global HOME, PROJECT_ROOT, VENV_DIR
    HOME = '/home/vagrant'
    PROJECT_ROOT = '/vagrant'
    VENV_DIR = os.path.join(HOME, '.virtualenvs')  

@task
def staging():  
    env.hosts = ['ashish_the_dev@35.200.201.121']
    env.environment = 'staging'

@task
def production():  
    env.hosts = ['ashish_the_dev@35.200.201.121']
    env.environment = 'production'

# DO NOT EDIT ANYTHING BELOW THIS LINE!

@contextmanager
def workon_virtualenv():  
    with prefix('workon ' + PROJECT_NAME):
        yield

def clean():  
    """Cleans Python bytecode"""
    sudo('find . -name \'*.py?\' -exec rm -rf {} \;')


def chown():  
    """Sets proper permissions"""
    sudo('chown -R www-data:www-data %s' % PROJECT_ROOT)


def restart():  
    sudo('systemctl restart nginx')
    #sudo('systemctl restart gunicorn')
    sudo('systemctl restart {}'.format(PROJECT_NAME))

def start():
    sudo('systemctl start emailer')

def stop():
    sudo('systemctl stop emailer')

@task
def deploy():  
    """
    Deploys the latest tag to the production server
    """
    sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        run('git pull origin master')
        run('git checkout m_vagrant')#TODO: Delete later
        with prefix('workon {}'.format(PROJECT_NAME)):
            sudo('pip install -r requirements/production.txt')

    chown()
    restart()


@task
def bootstrap():  
    """Bootstrap the latest code at the app servers"""
    sudo('apt-get update && apt-get -y install git nginx python3-dev python3-pip nginx gunicorn')
    sudo('pip install virtualenvwrapper')

    sudo('''sudo echo 'export WORKON_HOME=$HOME/.virtualenvs' >> ~/.bashrc ''')
    #sudo('''ln -s /usr/share/virtualenvwrapper/virtualenvwrapper.sh /usr/local/bin/virtualenvwrapper.sh''')#http://virtualenvwrapper.readthedocs.io/en/latest/install.html#python-versions
    sudo('''sudo echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc ''')
    sudo('rm -f /etc/nginx/sites-enabled/emailer.conf')
    sudo('rm -f /etc/systemd/system/multi-user.target.wants/emailer.service')
    sudo('rm -rdf {}'.format(VENV_DIR))
    sudo('rm -rdf {}'.format(PROJECT_ROOT))

    sudo('mkdir -p {}'.format(PROJECT_ROOT))
    sudo('chown -R {}:{} {}'.format(env.user, env.user, PROJECT_ROOT))

    sudo('mkvirtualenv {}'.format(PROJECT_NAME))
    run('git clone {} {}'.format(REPO, PROJECT_ROOT))#You need to use ssh.agent_forwarding or copy id files in .ssh
    run('git pull origin master')
    run('git checkout m_vagrant')#TODO: Delete later
    chown()

    with prefix('workon {}'.format(PROJECT_NAME)):
        sudo('pip install -r requirements.txt')

    sudo('systemctl enable nginx')
    sudo('systemctl enable gunicorn')


    #Systemd configuration
    sudo('ln -s {project_root}/deploy/{environment}/{project_name}.service /etc/systemd/system/multi-user.target.wants/{project_name}.service'.format(
        project_root=PROJECT_ROOT, environment=env.environment, project_name=PROJECT_NAME))

    #Nginx configuration
    sudo('ln -s {project_root}/deploy/{environment}/nginx.conf /etc/nginx/sites-enabled/{project_name}.conf'.format(
        project_root=PROJECT_ROOT, environment=env.environment, project_name=PROJECT_NAME))

    restart()