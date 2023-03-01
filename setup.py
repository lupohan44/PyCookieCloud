#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import sys

if sys.version_info[0] != 3:
    sys.exit('Python 2 is not supported')

setup(
    name='PyCookieCloud',
    license='MIT',
    version='1.0.0',
    author='lupohan44',
    author_email='cptf_lupohan@126.com',
    url='https://github.com/lupohan44/PyCookieCloud',
    description='This is an unofficial Python wrapper library for CookieCloud (https://github.com/easychen/CookieCloud).',
    keywords=['cookiecloud', 'cookie', 'cloud', 'cookies', 'cookiecloud-python', 'pycookiecloud'],
    packages=['PyCookieCloud'],
    install_requires=['requests', 'pycryptodome']
)