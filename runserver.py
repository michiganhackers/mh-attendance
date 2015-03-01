import os
import sys

def get_env_vars(filename):
    '''Import environment variables from filename with format key=value'''
    for line in open(filename):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

def setup_environment():
    """
    Loads the environment variables from the Envs/ folder.
    Specifically, ./Envs/.env-$ENV

    If this fails to find the ENV variable set, it defaults to 'dev'
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    envdir = os.path.join(basedir, 'Envs')
    env_file = os.path.join(envdir, '.env-')

    env = os.getenv('ENV', None)
    if env is None:
        print >> sys.stderr, "Warning: Environment variable 'ENV' is not set, "\
                             + "defaulting to development."
        env = 'dev'
    print 'Importing environment from %s' % env

    env_file += env
    get_env_vars(env_file)


setup_environment()
from app import create_app, db
from app.models import User, Event
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Event=Event)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
    '''Run the unit tests.'''
    COV = None
    if coverage:
        import coverage
        COV = coverage.coverage(branch=True, include='app/*')
        COV.start()
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('FLASK_CONFIG: ', os.getenv('FLASK_CONFIG'))
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
def create_db(mock=False):
    migrate()

    if mock:
        load_mock_data()

def load_mock_data():
    User.generate_fake(100)
    Event.generate_fake(100)

@manager.command
def recreate_db(mock=False):
    db.drop_all()
    create_db(mock=mock)


@manager.command
def migrate():
    '''Run deployment tasks.'''
    from flask.ext.migrate import upgrade

    # migrate database to latest revision
    upgrade()


if __name__ == '__main__':
    manager.run()
    app.run(debug=True)
