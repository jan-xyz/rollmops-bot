#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from setuptools import setup

PYTHON_PACKAGE_VERSION_MAJOR = '0'
PYTHON_PACKAGE_VERSION_MINOR = '0'
PYTHON_PACKAGE_VERSION_PATCH = '2'

setup(
    name='rollmops',
    version='%s.%s.%s' % (PYTHON_PACKAGE_VERSION_MAJOR,
                          PYTHON_PACKAGE_VERSION_MINOR,
                          PYTHON_PACKAGE_VERSION_PATCH),
    packages=['rollmops', 'tests'],
    install_requires=[],
    author="Jan Steinke, Jonas Pruditsch",
    author_email="jan.steinke@gmail.com, jonas.pruditsch@online.de",
    description="a mops that rolls your slack experience!",
    zip_safe=False,
    tests_require=['pytest>=2.9.2'],
)
