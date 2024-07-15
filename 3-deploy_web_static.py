#!/usr/bin/python3
"""
Creates and distributes an archive to web servers

function: deploy()
"""

from fabric import decorators
from fabric.api import env, put, run, local
from datetime import datetime
import os

env.user = "ubuntu"
env.hosts = ['100.25.194.252', '3.94.213.134']
env.key_filename = '~/.ssh/school'


def deploy():
    """Wrapper function to pack html files into tarball and transfer
    to web servers."""
    return do_deploy(do_pack())


@decorators.runs_once
def do_pack():
    """Generates a .tgz archive and saves with current date
    """
    current_time = datetime.utcnow().strftime(
        "%Y%m%d%H%M%S")
    archive_name = f"web_static_{current_time}.tgz"
    archive_path = f"versions/{archive_name}"

    local(f"mkdir -p versions")
    if local(f"tar -czvf {archive_path} web_static").failed:
        return None

    size = os.stat(archive_path).st_size
    print('web_static packed: {} -> {}Bytes'.format(archive_path, size))
    return archive_path


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

    try:
        put(archive_path, remote_tmp_path)
        remote_web_static_path = f"{remote_releases_path}{archive_filename}"
        run(f"mkdir -p {remote_web_static_path}")
        run(
            f"tar -xzf {remote_tmp_path}{archive} -C {remote_web_static_path}"
            )
        run(f"rm {remote_tmp_path}{archive}")
        run(f"mv \
                {remote_web_static_path}/web_static/* {remote_web_static_path}"
            )
        run(f"rm -rf {remote_web_static_path}/web_static")
        run(f"rm {symlink}")
        run(f"ln -s {remote_web_static_path} {symlink}")
        print('New version deployed!')
    except Exception as e:
        return False
    return True
