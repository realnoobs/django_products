#!/usr/bin/env python

import os
from setuptools import setup
from django_numerators import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-products',
    version=__version__,
    description='Django polymorphic products, tests included',
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer='Rizki Sasri Dwitama',
    maintainer_email='sasri.project@gmail.com',
    license="MIT",
    url='https://github.com/sasriawesome/django_products',
    packages=[
        'django_products',
        'django_products.migrations',
        'django_products.utils',
    ],
    install_requires=[
        'Django>=2.2',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    tes_suite="tests.run_tests.run_tests"
)
