#!/usr/bin/env python
from distutils.command.install import INSTALL_SCHEMES
import os

from setuptools import setup, find_packages

pkgs = ['kcontrol']

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

os.chdir(os.path.abspath(os.path.join(__file__, "..")))

setup(
    name="kcontrol",
    author="Jeremy Lowery",
    author_email="jeremy@koarcg.com",
    url="http://bitbucket.org/jslowery/kcontrol",
    zip_safe=False,
    packages = pkgs)
