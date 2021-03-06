#!/usr/bin/env python3
# coding: utf-8

import os
import re

from setuptools import setup, find_packages


# import joker; exit(1)
# DO NOT import your package from your setup.py

namespace = 'joker'
package_name = 'flasky'
description = 'Tweak flask for static site builiding'


def read(filename):
    with open(filename) as f:
        return f.read()


def version_find():
    if namespace:
        path = '{}/{}/__init__.py'.format(namespace, package_name)
    else:
        path = '{}/__init__.py'.format(package_name)
    root = os.path.dirname(__file__)
    path = os.path.join(root, path)
    regex = re.compile(
        r'''^__version__\s*=\s*('|"|'{3}|"{3})([.\w]+)\1\s*(#|$)''')
    with open(path) as fin:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            mat = regex.match(line)
            if mat:
                return mat.groups()[1]
    raise ValueError('__version__ definition not found')


config = {
    'name': '{}-{}'.format(namespace, package_name),
    'version': version_find(),
    'description': '' + description,
    'keywords': '',
    'license': "GNU General Public License (GPL)",
    'packages': find_packages(exclude=['test_*']),
    'zip_safe': False,
    'install_requires': read("requirements.txt"),
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # ensure copy static file to runtime directory
    'include_package_data': True,
}

if namespace:
    config['namespace_packages'] = [namespace]

setup(**config)

