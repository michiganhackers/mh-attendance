#!/usr/bin/env python
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

def get_env_vars(filename):
    '''Import environment variables from filename with format key=value'''
    for line in open(filename):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

# Set environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
envdir = os.path.join(basedir, 'Envs')

env_file = os.path.join(envdir, '.env')
if os.path.exists(env_file):
    
    get_env_vars(env_file)
    os.getenv('ENV')
    
    env = os.getenv('ENV')
    print 'Importing environment from %s' % env
    env_file = 'Envs/' + env
    get_env_vars(env_file)


from app import create_app, db
from flask.ext.script import Manager, Shell
# from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
# migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)
manager.add_command('shell', Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    '''Run the unit tests.'''
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@manager.command
def profile(length=25, profile_dir=None):
    '''Start the application under the code profiler.'''
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                        profile_dir=profile_dir)
    app.run()

@manager.command
def deploy():
    '''Run deployment tasks.'''
    pass
    # from flask.ext.migrate import upgrade

    # migrate database to latest revision
    # upgrade()


if __name__ == '__main__':
    manager.run()