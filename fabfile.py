from fabric.api import *

version = "0.1.5"
wheel = "kcontrol-{0}-py3-none-any.whl".format(version)
tarball = "kcontrol-{0}.tar.gz".format(version)

def build():
    local("python3 -m build")

def bumpver():
    local("bumpver update -p --commit")

def twine():
    local("twine upload dist/{0} dist/{1}".format(wheel, tarball))

def develop():
    local("python3 -m pip -e .")
