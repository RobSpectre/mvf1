from mvf1 import __version__

scripts = ['bin/mvf1-cli']

setup_args = {
    "name": "mvf1",
    "version": __version__,
    "url": "https://github.com/RobSpectre/mvf1",
    "description": "A Python package to control video players for "
                   "MultiViewer for F1, the best way to watch "
                   "Formula 1.",
    "long_description": open('README.rst').read(),
    "author": "Rob Spectre",
    "author_email": "rob@brooklynhacker.com",
    "license": "MIT",
    "packages": ["mvf1", "tests"],
    "scripts": ["bin/mvf1-cli"],
    "include_package_data": True,
    "classifiers": [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Console',
    ]
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(**setup_args)
