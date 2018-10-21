#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for kryptoflow.

    This file was generated with PyScaffold 3.0.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: http://pyscaffold.org/
"""

from setuptools import setup, find_packages
from pathlib import Path  # noqa

NAME = 'kryptoflow'
README = Path('README.md')
EXTENSIONS = {
    'aws',
    'tf',
    'tf_gpu',
    'nlp',
    'test'
}


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req, *root):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*root, *path.split('/'))
    return [req]


def _reqs(*f):
    path = (Path.cwd() / 'requirements').joinpath(*f)
    with path.open() as fh:
        reqs = [strip_comments(l) for l in fh.readlines()]
        return [_pip_requirement(r, *f[:-1]) for r in reqs if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]


def extras(*p):
    """Parse requirement in the requirements/extras/ directory."""
    return reqs('extras', *p)


def extras_require():
    """Get map of all extra requirements."""
    return {x: extras(x + '.txt') for x in EXTENSIONS}


# -*- Long Description -*-


if README.exists():
    long_description = README.read_text(encoding='utf-8')
else:
    long_description = 'See http://pypi.org/project/{}'.format(NAME)

# -*- Install Requires -*-


install_requires = reqs('default.txt')


def setup_package():
    setup(version='0.5.1',
          include_package_data=True,
          install_requires=install_requires,
          tests_require=extras('test.txt'),
          extras_require=extras_require(),
          keywords=[
              'kryptoflow',
              'tensorFlow',
              'deep-learning',
              'machine-learning',
              'data-science',
              'bitcoin',
              'kafka',
              'time-series'
          ],
          entry_points={"console_scripts": [
                  "kryptoflow = kryptoflow.main:cli",
              ],
          },
          classifiers=[
              'Programming Language :: Python',
              'Operating System :: OS Independent',
              'Intended Audience :: Developers',
              'Intended Audience :: Science/Research',
              'Topic :: Scientific/Engineering :: Artificial Intelligence'
          ],
          # dependency_links=['https://github.com/Supervisor/supervisor/tarball/master#egg=supervisor-4.0.0.dev',
          #                   'https://github.com/carlomazzaferro/coinbasepro-python/tarball/master#egg=coinbasepro-python-1.1.2'],
          dependency_links=['git+git://github.com/Supervisor/supervisor.git@master#egg=supervisor-4.0.0.dev'],


          packages=find_packages(),
          )


if __name__ == "__main__":
    setup_package()
