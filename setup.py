#! /usr/bin/env python

from setuptools import setup
setup(
    name='Viento',
    version='0.6.0',
    author='Tiger Sachse',
    author_email='tgsachse@gmail.com',
    description='A CLI tool to sync files between local and remote directories',
    long_description='test',#long_description,
    url='https://github.com/tgsachse/viento',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Desktop Environment :: File Managers'],
    keywords='rclone cloud storage remote access CLI',
    packages=['viento'],
    install_requires=['termcolor'],
    python_requires='>=3',
    data_files=[('bin',['viento/viento']),
                ('share/man/man1',['docs/viento.1'])],

    )
