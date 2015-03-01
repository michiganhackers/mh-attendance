import os

preload = True
bind = "127.0.0.1:8000"
daemon = True
workers = 4

LOGDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')

loglevel = "info"
accesslog = os.path.join(LOGDIR, 'server-access-log.log')

loglevel = "error"
errorlog = os.path.join(LOGDIR, 'gunicorn-error.log')
