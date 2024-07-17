#!/usr/bin/python3
"""
Distributes an archive to the web servers

function: do_deploy()
"""
from fabric.api import env, put, run, sudo
import os

env.user = "ubuntu"
env.hosts = ['107.23.46.106', '3.94.213.134']


def do_deploy(archive_path):
    """Distributes an archive to the web servers

    Args:
        archive_path (str): path of the .tgz file to transfer

    Returns: True on success, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    archive = archive_path.split("/")[-1]
    # Get the filename without extension
    archive_filename = archive.split(".")[0]
    remote_tmp_path = "/tmp/"
    remote_releases_path = "/data/web_static/releases/"
    symlink = "/data/web_static/current"
    root = "/var/www/html/web_static"

    try:
        put(archive_path, remote_tmp_path)
        remote_web_static_path = f"{remote_releases_path}{archive_filename}"
        sudo(f"mkdir -p {remote_web_static_path}")
        # Uncompress the archive to the /data/web_static/releases/ directory
        sudo(
            f"tar -xzf {remote_tmp_path}{archive} -C {remote_web_static_path}"
            )
        # Remove archive from the web server
        sudo(f"rm {remote_tmp_path}{archive}")
        # Copy web_static to the specific release
        sudo(f"mv \
                {remote_web_static_path}/web_static/* {remote_web_static_path}"
            )
        sudo(f"rm -rf {remote_web_static_path}/web_static")
        # Delete symbolic link and create new one
        sudo(f"if [ -L {symlink} ]; then rm {symlink}; fi")
        sudo(f"ln -s {remote_web_static_path} {symlink}")
        sudo(f"ln -s {symlink} {root}")
        print('New version deployed!')
    except Exception as e:
        return False
    return True
