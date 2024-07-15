#!/usr/bin/env bash

from fabric import task
from fabric.api import run, env
from fabric.contrib.files import exists
import operator
import os

env.user = "ubuntu"
env.hosts = ['100.25.194.252', '3.94.213.134']
env.key_filename = '~/.ssh/school'


@task
def do_clean(c, number=0):
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
