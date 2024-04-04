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
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = 'versions/web_static_{}.tgz'.format(date)
    arch_path = local('tar -cvzf {} web_static'.format(file_name))

    if arch_path.succeeded:
        return file_name
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if os.path.exists(archive_path):
        new_name = '/data/web_static/releases/{}/'.format(archive_path[9:-4])
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}'.format(new_name))
        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_path[9:], new_name))
        run('sudo rm /tmp/{}'.format(archive_path[9:]))
        run('sudo mv {}/web_static/* {}'.format(new_name, new_name))
        run('sudo rm -rf {}/web_static'.format(new_name))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(new_name))
        print("New version deployed!")
        return True

    return False
