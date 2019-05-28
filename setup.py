#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
setup file for dids
"""

from setuptools import setup, find_packages

with open('requirements.txt') as stream:
    REQUIREMENTS = stream.read().splitlines()

setup(
    name='anomaly',
    version='1.0.0',
    description="An example to detect anomalies",
    author="G. Broccolo",
    author_email='gbroccolo@decibelinsight.com',
    url='',
    packages=find_packages(),
    package_dir={
        'anomaly': 'anomaly',
    },
    entry_points={
        'console_scripts': [
            'flask_wrapper=flask_wrapper:main',
            'anomaly=anomaly.anomaly:main',
        ]
    },
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False,
    keywords='anomaly',
    classifiers=[],
)
