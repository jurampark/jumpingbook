from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm
from fabric.contrib.files import exists

env.hosts = ['54.92.86.110']
env.user = 'ec2-user'
env.key_filename = '~/.ssh/ramju.pem'

git_repo_url = "git@github.com:parkjuram/jumpingbook.git"
remote_root_directory  = '~/workspace/django/jumpingbook'
remote_git_directory = remote_root_directory + '/source'
remote_source_directory = remote_root_directory + '/source/jumpingbook'
remote_virtualenv_directory = remote_root_directory + '/virtualenv'

def _test():
    with settings(warn_only=True):
        test_result = local("./manage.py test my_app",capture=True)
    if test_result.faild and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def prepare_deploy():
    # _test();
    with settings(warn_only=True):
        local("git add -p && git commit")
        local("git push")

def _create_directory_if_necessary():
    for subfoler in ('database', 'static', 'source', 'virtualenv'):
        run('mkdir -p %s/%s' % (remote_root_directory, subfoler))

def _get_latest_source():
    if exists(remote_git_directory + '/.git'):
        with cd(remote_git_directory):
            run("git pull")
    else:
        run("git clone %s %s" % (git_repo_url, remote_git_directory) )
        
def _update_virtualenv():
    if not exists(remote_virtualenv_directory+'/bin/pip'):
        run('virtualenv --python=pytohn2.7.6 %s' % (remote_virtualenv_directory))
    run('%s/bin/pip install -r %s/requirements.txt' % (remote_virtualenv_directory, remote_source_directory))

def _update_static_files():
    with cd(remote_source_directory):
        run('%s/bin/python manage.py collectstatic --noinput' % remote_virtualenv_directory )

def _update_database():
    with cd(remote_source_directory):
        run('%s/bin/python manage.py syncdb' % remote_virtualenv_directory )

def deploy():
    _create_directory_if_necessary()
    _get_latest_source()
    _update_virtualenv()
    _update_static_files()
    _update_database()
