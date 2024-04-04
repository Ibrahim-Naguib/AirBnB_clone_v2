#!/usr/bin/python3
"""
script that generates a .tgz archive from the contents of the web_static folder
"""
from fabric.api import local
from datetime import datetime
import os


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
