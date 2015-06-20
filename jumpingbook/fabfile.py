from fabric.api import local
from fabric.context_managers import settings


def prepare_deploy():
    # local("./manage.py test my_app")
    with settings(warn_only=True):
        local("git add -p && git commit")
        local("git push")