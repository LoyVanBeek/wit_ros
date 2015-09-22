#!/usr/bin/env python

# DO NOT USE
# python setup.py install
# roslaunch the node

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup()
d['packages'] = ['wit_ros']
d['package_dir'] = {'':'src'}

setup(**d)
