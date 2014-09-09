import sys

activate_this = '/home/ec2-user/Envs/mh-attendance-venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, '/var/www/mh-attendance')

from manage import app as application