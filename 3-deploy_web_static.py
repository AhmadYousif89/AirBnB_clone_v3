#!/usr/bin/python3
"""
Fabric script that creates and uploads an archive to the web servers
Usage: fab -f 3-deploy_web_static.py deploy -i ssh_private_key
"""

from datetime import datetime
from os.path import exists, join
from fabric.api import env, local, put, run, runs_once

env.user = 'ubuntu'
env.hosts = ['34.224.62.175', '54.157.181.100']

src_folder = 'web_static'
dest_folder = 'versions'


@runs_once
def do_pack():
    """making an archive on web_static folder"""
    time = datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S")
    archive_name = '{}_{}.tgz'.format(src_folder, timestamp)
    save_path = join(dest_folder, archive_name)
    try:
        local('mkdir -p {}'.format(dest_folder))
        local('tar -cvzf {} {}'.format(save_path, src_folder))
        return archive_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Uploads an archive to the web servers"""
    archive_fullpath = '{}/{}'.format(dest_folder, archive_path)
    if not exists(archive_fullpath):
        return False

    archive_name = archive_path.split('.')[0]  # web_static_20240505004540
    archive_tmp_path = "/tmp/{}".format(archive_path)
    release_path = "/data/web_static/releases/{}".format(archive_name)

    try:
        put(archive_fullpath, archive_tmp_path)
        run("mkdir -p {}".format(release_path))
        unpack = 'tar -xzf {} -C {} --strip-components=1'.format(
            archive_tmp_path, release_path
        )
        run(unpack)
        run("rm {}".format(archive_tmp_path))
        run("rm -rf /data/web_static/current")
        run("ln -sf {} /data/web_static/current".format(release_path))
        return True
    except Exception:
        return False


def deploy():
    """creates and deploy a new web_static release to the web servers"""
    archive_path = do_pack()  # web_static_20240505004540.tgz
    if archive_path is None:
        print("Failed to create the archive")
        return False
    return do_deploy(archive_path)
