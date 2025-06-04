scripts = ['bin/mvf1-cli']

setup_args = {
    "name": "mvf1",
    "version": "2.0.0",
    "url": "https://github.com/RobSpectre/mvf1",
    "description": "A Python package and MCP server to control "
                   "video players for MultiViewer, the best way"
                   "to watch motorsports like Formula 1.",
    "long_description": open('README.rst').read(),
    "author": "Rob Spectre",
    "author_email": "rob@brooklynhacker.com",
    "license": "MIT",
    "packages": ["mvf1", "tests"],
    "scripts": ["bin/mvf1-cli"],
    "include_package_data": True,
    "install_requires": ["click", "sgqlc", "fastmcp"],
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
