import os

from fabric.api import *
from contextlib import contextmanager

SRC_DIR = os.path.abspath(os.path.dirname(__file__))

env.ENV = None

@task
def dev():
    env.ENV = 'dev'

@task
def prod():
    env.ENV = 'prod'

@task
def test():
    env.ENV = 'test'

@task
def clean():
    local('find . -type f -name "*.pyc" -exec rm -f {} \;')

@task
def setup():
    """Install requirements"""
    with lcd(SRC_DIR):
        print "SRC_DIR: %s" % SRC_DIR
        local('virtualenv env')
        virtualenv('pip install -r requirements.txt')
        gen_dev_env_config()
        create_db()

@task
def pip_freeze():
    """Freeze pip install modules"""
    virtualenv("./env/bin/pip freeze > requirements.txt")


@task
def run_dev():
    """Start a local staging server"""
    dev()
    with lcd(SRC_DIR), shell_env(ENV='dev'):
        virtualenv("python runserver.py runserver")

@task
def run_production():
    """Start the production server"""
    prod()
    with lcd(SRC_DIR), shell_env(ENV='prod'):
    	local("cp ../mh-attendance-envs/.env-prod ./Envs/.env-prod")
        virtualenv("exec gunicorn -c gunicorn-conf.py runserver:app")

@task
def gen_dev_env_config():
    """Creates a default development config file"""
    with lcd(SRC_DIR):
        local('mkdir -p ./Envs/')
        local('touch ./Envs/.env-dev')

        # Not required, so only warn if not there
        with settings(warn_only=True):
            copy_env()

@task
def copy_env():
    local('cp -r ../mh-attendance-envs/.env* Envs/')

@task
def migrate():
    """Runs database migrations"""
    virtualenv("python runserver.py migrate")

@task
def create_db(mock=False):
    """Creates initial databases. If mock is True, fills with mock data."""
    virtualenv("python runserver.py create_db")


@contextmanager
def workon():
    """Activates the virtualenv"""
    with lcd(SRC_DIR):
        with prefix("/bin/bash -l -c 'source ./env/bin/activate'"):
            with shell_env(ENV=env.ENV):
                yield

@task
def runserver_cmd(cmd):
    """Run command defined in runserver.py"""
    cmd = "python runserver.py " + cmd
    virtualenv(cmd)

@task
def virtualenv(cmd):
    """Runs a command in the virtualenv """
    if env.ENV is None:
        print "You didn't specify the role. Defaulting to 'dev'"
        env.ENV = 'dev'

    with shell_env(ENV=env.ENV):
        local("/bin/bash -l -c 'source ./env/bin/activate && {}'".format(cmd))

