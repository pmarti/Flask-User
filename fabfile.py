from fabric.operations import local
from fabric.api import cd, env, task, prefix, run
from contextlib import contextmanager

@task
def runserver():
    local('python runserver.py')

@task
def test():
    # Requires "pip install pytest"
    local('py.test flask_user/tests/')

@task
def coverage():
    # Requires "pip install pytest-coverage"
    local('py.test --cov flask_user --cov-report term-missing --cov-config flask_user/tests/.coveragerc flask_user/tests/')

@task
def docs():
    local('cp example_apps/*_app.py docs/source/includes/.')
    local('sphinx-build -b html docs/source ../builds/flask_user/docs')
    local('cd ../builds/flask_user/docs && zip -u -r flask_user_docs *')

@task
def rebuild_docs():
    local('rm -fr ../builds/flask_user/docs')
    docs()

@task
def upload_to_pypi():
    local('python setup.py sdist upload')
