#!/usr/bin/env python3

"""
Cement package setup.
"""

from cement.utils import version

from setuptools import find_packages, setup

VERSION = version.get_version()


def get_readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="cement",
    version=VERSION,
    python_requires=">=3.6",
    description="Application Framework for Python",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    install_requires=["jinja2", "pandas", "pysocks", "PyYAML"],
    keywords="cli framework",
    author="Data Folk Labs, LLC",
    author_email="derks@datafolklabs.com",
    url="https://builtoncement.com",
    license="BSD",
    packages=find_packages(exclude=["tests*"]),
    package_data={"cement": ["cement/cli/templates/generate/*"]},
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["cement = cement.cli.main:main"]},
)
