import os
import re
from fabric.api import run, local, lcd, cd, put, env

_version_re = re.compile("^\s*version=['\"]([^'\"]+)")
def get_version():
    for line in open("setup.py"):
        match = _version_re.match(line)
        if match:
            return match.groups()[0]

def update(revision='tip'):
    """ Update the development system. """
    local("python setup.py install --prefix=/usr/local")
    local("python3 setup.py install --prefix=/usr/local")
    local("rm -rf build")

def deploy(revision='tip'):
    """ Deploy the command line tools to the backend server and the
    python library to the client server
    """
    version = get_version()

    # Clean out working directory
    if os.path.exists("/tmp/kcontrol"):
        local("rm -rf /tmp/kcontrol")

    # Pull source code from repository
    local("hg clone -qr %s . /tmp/kcontrol" % revision)

    # Build a source distribution
    with lcd("/tmp/kcontrol"):
        local("python setup.py --quiet sdist")
        local("python3 setup.py --quiet sdist")

    # Send to remote host
    tarball = "/tmp/kcontrol/dist/kcontrol-%s.tar.gz" % version
    put(tarball, "/tmp")

    # untar
    with cd("/tmp"):
        run("tar xzf kcontrol-%s.tar.gz" % version)

    # setup
    with cd("/tmp/kcontrol-%s" % version):
        run("python setup.py --quiet install --prefix=/usr/local")

    # cleanup
    run("rm -rf /tmp/kcontrol-%s" % version)
    run("rm -f /tmp/kcontrol-%s.tar.gz" % version)
    local("rm -rf /tmp/kcontrol")
