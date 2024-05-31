#!/usr/bin/python3
"""
Deletes out-of-date archives
fab -f 100-clean_web_static.py do_clean:keep=2 -i ssh-key > /dev/null 2>&1
"""

import os
from fabric.api import run, cd, lcd, local, env

env.user = 'ubuntu'
env.hosts = ['54.157.181.100', '34.224.62.175']


def do_clean(keep=0):
    """Delete out-of-date archives.
    Args:
        keep (int): The number of archives to keep.
    If (keep) is 0 or 1, it will keep only the most recent archive.
    If (keep) is 2 or more, it will keep the most recent (n of keep) archives.
    """
    archives_path = "versions"
    keep = 1 if int(keep) == 0 else int(keep)
    archives = sorted(os.listdir(archives_path))
    with lcd(archives_path):
        for archive in archives[-keep:]:
            local("rm -rf ./{}".format(archive))

    releases_path = "/data/web_static/releases"
    with cd(releases_path):
        output = run("ls -tr").split()
        archives = [archive for archive in output if "web_static" in archive]
        for archive in archives[-keep:]:
            run("rm -rf ./{}".format(archive))
