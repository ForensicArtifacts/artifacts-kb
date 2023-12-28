#!/bin/bash
#
# Script that makes changes in preparation of a new release, such as updating
# the version and documentation.

EXIT_FAILURE=1;
EXIT_SUCCESS=0;

VERSION=`date -u +"%Y%m%d"`

# Update the Python module version.
sed "s/__version__ = '[0-9]*'/__version__ = '${VERSION}'/" -i artifactsrc/__init__.py

# Update the version in the setuptools configuration.
sed "s/version = [0-9]*/version = ${VERSION}/" -i setup.cfg

# Regenerate the API documentation.
tox -edocs

exit ${EXIT_SUCCESS};

