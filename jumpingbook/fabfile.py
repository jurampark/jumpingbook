from fabric.api import local

def prepare_deploy():
    # local("./manage.py test my_app")
    local("git add -p && git commit --allow-empty")
    local("git push")