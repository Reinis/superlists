import os
import random

from fabric.api import env, lcd, local, task


REPO_URL = 'https://github.com/Reinis/superlists.git'



@task
def deploy(site_name):
    site_folder = '/home/%s/sites/%s' % (env.user, site_name)
    source_folder = site_folder + '/source'
    create_directory_structure_if_necessary(site_folder)
    get_latest_source(source_folder)
    update_settings(source_folder, site_name)
    update_wsgi(source_folder, env.user)
    update_virtualenv(source_folder)
    update_static_files(source_folder)
    update_database(source_folder)


def create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'source', 'static', 'virtualenv'):
        local('mkdir -p %s/%s' % (site_folder, subfolder))


def get_latest_source(source_folder):
    with lcd(source_folder):
        if os.path.exists('.git'):
            local('git reset --hard')
            local('git pull')
        else:
            local('git clone %s %s' % (REPO_URL, source_folder))


@task
def update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    local("sed -e 's#DEBUG = True#DEBUG = False#' -i '%s'" % (settings_path,))
    local("sed -e 's#ALLOWED_HOSTS =.*$#ALLOWED_HOSTS = \[\"%s\"\]#' -i '%s'" % (site_name, settings_path))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not os.path.exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        local("echo 'SECRET_KEY = \"%s\"' > '%s'" % (key, secret_key_file))
    local("sed -e 's#SECRET_KEY =.*$#from .secret_key import SECRET_KEY#' -i '%s'" % (settings_path,))


def update_wsgi(source_folder, user_name):
    wsgi_conf_file = "/var/www/%s_pythonanywhere_com_wsgi.py" % (user_name,)
    s  = "echo \"import path\n"
    s += "path = '%s'\n"
    s += "if path not in sys.path:\n"
    s += "    sys.path.append(path)\n\" > '%s'"
    local(s % (source_folder, wsgi_conf_file))
    local("cat '%s' >> '%s'" % (source_folder + '/superlists/wsgi.py', wsgi_conf_file))


def update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not os.path.exists(virtualenv_folder + '/bin/pip'):
        local("virtualenv -p python3.4 '%s'" %(virtualenv_folder,))
    local("'%s'/bin/pip install -r '%s'/requirements.txt" % (virtualenv_folder, source_folder))


def update_static_files(source_folder):
    with lcd(source_folder):
        local("../virtualenv/bin/python3 manage.py collectstatic --noinput")


def update_database(source_folder):
    with lcd(source_folder):
        local("../virtualenv/bin/python3 manage.py migrate --noinput")

