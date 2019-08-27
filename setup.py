#!/usr/bin/env python
# Learn more: https://github.com/kennethreitz/setup.py
import os
import re
import sys

from setuptools import setup


# 'setup.py publish' shortcut.
if len(sys.argv) == 3 and sys.argv[-2] == "publish":
    os.system("python setup.py sdist upload --repository " + sys.argv[-2])
    sys.exit()


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="is-denorm",
    version="0.0.1",
    description="is-denorm is a denormalizer for Icelandic",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=["denorm"],
    package_dir={"denorm": "denorm"},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    tests_require=["pytest>=3"],
)
