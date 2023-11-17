from setuptools import setup

setup(
    name="kcontrol",
    version="0.1.4",
    provides=["kcontrol"],
    description="Simple html control library",
    license="MIT License",
    author="Jeremy Lowery",
    author_email="jeremy@bitrel.com",
    url="https://github.com/jeremylowery/kcontrol",
    platforms="All",
    classifiers=[
        "Development Status :: 5 - Beta",
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
