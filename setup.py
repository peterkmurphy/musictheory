#!/usr/bin/env python
     
from distutils.core import setup

setup(
    name='musictheory',
    version='0.5',
    author='Peter Murphy',
    author_email='peterkmurphy@gmail.com',
    packages=['musictheory'],
    url='http://pypi.python.org/pypi/musictheory/',
    license='LICENSE.txt',
    description='Provides classes for "music set theory"-like analysis.',
    keywords='music set theory temperament scale chords',
    long_description=open('README.txt').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Artistic Software',
        'Topic :: Education',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Software Development',
        'Topic :: Utilities',
        ],
)     
