#!/usr/bin/python3
"""
script that distributes an archive to the web servers
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['54.236.30.138', '100.25.188.43']


def do_pack():
    """Generates a .tgz archive"""
    try:
        if isdir("versions") is False:
            local("mkdir versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = 'versions/web_static_{}.tgz'.format(date)
        local('tar -cvzf {} web_static'.format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if os.path.exists(archive_path) is False:
        return False
    try:
        old_name = archive_path.split("/")[-1]
        new_name = old_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}'.format(path, new_name))
        run('sudo tar -xzf /tmp/{} -C {}{}'.format(old_name, path, new_name))
        run('sudo rm /tmp/{}'.format(old_name))
        run('sudo mv {0}{1}/web_static/* {0}{1}'.format(path, new_name))
        run('sudo rm -rf {}{}/web_static'.format(path, new_name))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{} /data/web_static/current'.format(path, new_name))
        return True
    except:
        return False


def deploy():
    """Distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
