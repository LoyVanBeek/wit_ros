#!/usr/bin/env python

from setuptools import setup

setup(  name='wit_ros',
        version='0.1.0',
        author='Loy van Beek',
        author_email='loy.vanbeek@gmail.com',
        scripts=['src/wit_ros/wit_ros.py'],
        url='http://github.com/yol/wit_ros',
        license='LICENSE.txt',
        description='ROS wrapper around the Wit.ai NLP API',
        long_description=open('README.md').read(),
        install_requires=["requests"]
)
