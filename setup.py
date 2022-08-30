#!/usr/bin/env python
"""
CrawlerDetect setup file.
"""
import configparser
import os
import platform
import sys

from setuptools import setup

if sys.version_info[0] < 3:
    raise Exception(
        "You are tying to install CrawlerDetect on Python version {}.\n"
        "Please install CrawlerDetect in Python 3 instead.".format(
            platform.python_version()
        )
    )

config = configparser.ConfigParser()

current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, "setup.cfg")

config.read(config_file_path)

VERSION = config["crawlerdetect"]["version"]
AUTHOR = config["crawlerdetect"]["author"]
AUTHOR_EMAIL = config["crawlerdetect"]["email"]
URL = config["crawlerdetect"]["url"]

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

REQUIREMENTS = []
DEPENDENCIES = []

with open("requirements.txt") as requirements:
    for requirement in requirements.readlines():
        if requirement.startswith("git+git://"):
            DEPENDENCIES.append(requirement)
        else:
            REQUIREMENTS.append(requirement)


setup(
    name="crawlerdetect",
    version=VERSION,
    url=URL,
    download_url="{}/tarball/{}".format(URL, VERSION),
    project_urls={
        "Documentation": "https://crawlerdetect.readthedocs.io",
    },
    description="CrawlerDetect is a Python class for detecting bots/crawlers/spiders via the user agent.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=[
        "crawlerdetect",
        "crawlerdetect.src",
        "crawlerdetect.src.providers",
    ],
    package_dir={"crawlerdetect": "crawlerdetect"},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    dependency_links=DEPENDENCIES,
    python_requires=">=3.4, <4",
    license="BSD",
    zip_safe=True,
    platforms=["any"],
    keywords=[
        "crawler",
        "crawler detect",
        "crawler detector",
        "crawlerdetect",
        "python crawler detect",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Internet",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    test_suite="tests",
)
