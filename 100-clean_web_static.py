#!/usr/bin/python3

from fabric import task
from fabric.api import run, env
from fabric.contrib.files import exists
import operator
import os

env.user = "ubuntu"
env.hosts = ['107.23.46.106', '3.94.213.134']
env.key_filename = '~/.ssh/school'


@task
def do_clean(c, number=0):
    """
    Cleans up old versions of the web static files.

    Args:
        c (fabric.Connection): The fabric connection object.
        number (int, optional): The number of versions to keep. Defaults to 0.

    Returns:
        bool: True if the cleanup is successful, False otherwise.
    """
    number = int(number)

    if number < 1:
        number = 1

    try:
        number += 1
        local_archives = sorted(os.listdir("versions"))

        with c.cd("/data/web_static/releases"):
            remote_archives = sorted(c.run("ls -1t").stdout.split())

            for item in local_archives[number:]:
                if item in remote_archives:
                    c.run(f"rm -rf {item}")
                c.run(f"rm -rf /data/web_static/current")

        with c.cd("versions"):
            for item in local_archives[number:]:
                c.run(f"rm -rf {item}")
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

    return True
