#!/usr/bin/env python
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from distutils.core import setup
import numword

setup(name='numword',
        version=numword.__version__,
        author='B2CK',
        author_email='info@b2ck.com',
        url="http://code.google.com/p/numword/",
        description="Python modules to convert numbers to words. Easily extensible.",
        download_url="http://code.google.com/p/numword/downloads/",
        packages=['numword'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
            'Natural Language :: English',
            'Natural Language :: French',
            'Natural Language :: German',
            'Natural Language :: Spanish',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Internationalization',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Localization',
            'Topic :: Text Processing :: Linguistic',
            ],
        license='LGPL',
    )
