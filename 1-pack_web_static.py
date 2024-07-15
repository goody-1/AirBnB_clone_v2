#!/usr/bin/python3
"""
Generates a .tgz archive from the contents of the web_static folder

function: do_pack()
"""
import os
from datetime import datetime

from fabric.api import local


def do_pack():
    """Generates a .tgz archive and saves with current date"""
    current_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{current_time}.tgz"
    archive_path = f"versions/{archive_name}"

    local("mkdir -p versions")
    if local(f"tar -czvf {archive_path} web_static").failed:
        return None

    size = os.stat(archive_path).st_size
    print("web_static packed: {} -> {}Bytes".format(archive_path, size))
    return archive_path
