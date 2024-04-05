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
    if not os.path.isdir('versions'):
        os.mkdir('versions')

    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = 'versions/web_static_{}.tgz'.format(date)

    try:
        print('Packing web_static to {}'.format(file_name))
        local('tar -cvzf {} web_static'.format(file_name))
        file_size = os.path.getsize(file_name)
        print('web_static packed: {} -> {}Bytes'.format(file_name, file_size))
    except Exception:
        file_name = None
    return file_name


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if os.path.exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
