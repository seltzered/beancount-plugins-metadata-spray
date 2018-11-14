
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

INSTALL_REQUIRES = (
)

setup(
    name='beancount-plugins-metadata-spray',
    version='0.0.1',
    description="Beancount Plugin to add metadata to accounts",
    long_description="",
    license='GPLv2',
    author='Vivek Gani',
    author_email='me@vivekgani.com',
    url='https://github.com/seltzered/beancount-plugins-metadata-spray',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Financial and Insurance Industry',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
    install_requires=INSTALL_REQUIRES,
    packages=['beancount_plugins_metadata_spray',
              'beancount_plugins_metadata_spray.plugins',
              ],
    zip_safe=False,
)
