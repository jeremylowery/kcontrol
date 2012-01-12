#!/usr/bin/env python
import os

from distutils.core import setup


os.chdir(os.path.abspath(os.path.join(__file__, "..")))

setup(
    name="kcontrol",
    version="0.1.2",
    provides=["kcontrol"],
    description="Simple html control library",
    license="MIT License",
    author="Jeremy Lowery",
    author_email="jeremy@thensys.com",
    url="http://bitbucket.org/jslowery/kcontrol",
    platforms="All",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",   
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: All"
    ],
    packages = [
        'kcontrol',
        'kcontrol.Controls', 
        'kcontrol.util']
    )
