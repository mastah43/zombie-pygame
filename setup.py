#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from refdata_sim.polyglot_version import __version__

with open('requirements.txt', mode='r') as f:
    requirements = f.readlines()

setup(
    name='refdata-simulator',
    version=__version__,
    python_requires='>=3.7.0',
    packages=find_packages(),
    license='BMW AG',
    install_requires=requirements,
    entry_points={'console_scripts': [
        'refdatasim_gui=refdata_sim.export:export_pipeline',
    ]},
    url='https://cc-github.bmwgroup.net/swh/data-management/tree/master/refdata/refdata-simulator',
    author='Team Hopper (Area H Data Management)',
    author_email='EV-CCT-Hopper@list.bmw.com',
    package_data={
        '': ['*.json']
    }
)
