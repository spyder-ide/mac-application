# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Create a stand-alone Mac OS X app using py2app

To be used like this:
$ python setup.py py2app   (to build the app)
"""

import os
import sys
import shutil
import pkg_resources
from logging import getLogger, StreamHandler, Formatter
from setuptools import setup
from dmgbuild import build_dmg

fmt = Formatter('%(asctime)s [%(levelname)s] [%(name)s] -> %(message)s')
h = StreamHandler()
h.setFormatter(fmt)
logger = getLogger('Spy-Mac-App')
logger.addHandler(h)
logger.setLevel('INFO')

here = os.path.abspath(__file__)
this_repo = os.path.dirname(here)
basedir = os.path.dirname(this_repo)
distdir = os.path.join(this_repo, 'dist')
spy_repo = os.path.join(basedir, 'spyder')
ker_repo = os.path.join(basedir, 'spyder-kernels')

# copy spyder and spyder-kernels to repo
shutil.rmtree('spyder', ignore_errors=True)
shutil.rmtree('spyder_kernels', ignore_errors=True)
shutil.copytree(os.path.join(spy_repo, 'spyder'), 'spyder')
shutil.copytree(os.path.join(ker_repo, 'spyder_kernels'), 'spyder_kernels')

from spyder import __version__ as spy_version
from spyder.config.utils import EDIT_FILETYPES, _get_extensions
from spyder.config.base import MAC_APP_NAME

# parse additional arguments
make_app = True if 'py2app' in sys.argv else False
make_alias = True if '-A' in sys.argv else False
make_lite = False
make_dmg = True
if '--lite' in sys.argv:
    make_lite = True
    sys.argv.remove('--lite')
if '--no-dmg' in sys.argv:
    make_dmg = False
    sys.argv.remove('--no-dmg')

iconfile = os.path.join(spy_repo, 'img_src', 'spyder.icns')

py_ver = [sys.version_info.major, sys.version_info.minor,
          sys.version_info.micro]

#==============================================================================
# App Creation
#==============================================================================
APP_MAIN_SCRIPT = MAC_APP_NAME[:-4] + '.py'
shutil.copy2(os.path.join(spy_repo, 'scripts', 'spyder'), APP_MAIN_SCRIPT)

APP = [APP_MAIN_SCRIPT]
PACKAGES = [
    # The following packages cannot be in Resources/lib/pythonXX.zip
    # Error message: [Errno 20] Not a directory: '<path>/Resources/lib/
    # python38.zip/alabaster'
    'alabaster',
    # ImportError: cannot import name 'context' from 'astroid'
    # (<path>/Resources/lib/python38.zip/astroid/__init__.pyc)
    'astroid',
    # ModuleNotFoundError: No module named 'ipykernel.datapub'
    'ipykernel',
    # jedi.api.environment.InvalidPythonEnvironment: Could not get version
    # information for '<path>/Contents/MacOS/python': InternalError("The
    # subprocess <path>/Contents/MacOS/python has crashed (EOFError('Ran out
    # of input'), stderr=).")
    'jedi',
    # No module named 'jinja2.ext'
    'jinja2',
    # ModuleNotFoundError: No module named 'keyring.backends.<mod>'
    'keyring',
    # NotADirectoryError: [Errno 20] Not a directory:
    # '<path>/Resources/lib/python38.zip/parso/python/grammar38.txt'
    'parso',
    # ModuleNotFoundError: No module named 'pygments.formatters.latex'
    'pygments',
    # <path>/Contents/MacOS/python: No module named pyls
    # Note: still occurs in alias mode
    'pyls',
    # NotADirectoryError: [Errno 20] Not a directory: '<path>/Resourses/lib/
    # python38.zip/qtawesome/fonts/fontawesome4.7-webfont.ttf'
    'qtawesome',
    # NotADirectoryError: [Errno 20] Not a directory: '<path>/Resources/lib/
    # python38.zip/spyder/app/mac_stylesheet.qss'
    'spyder',
    # No module named spyder_kernels.console.__main__
    'spyder_kernels',
    # No module named 'sphinx.builders.changes'
    'sphinx',
    ]

if make_lite:
    INCLUDES = []
    EXCLUDES = ['numpy', 'scipy', 'pandas', 'matplotlib', 'cython', 'sympy']
else:
    INCLUDES = ['numpy', 'scipy', 'pandas', 'matplotlib', 'cython', 'sympy']
    EXCLUDES = []

EDIT_EXT = [ext[1:] for ext in _get_extensions(EDIT_FILETYPES)]

OPTIONS = {
    'optimize': 0,
    'packages': PACKAGES,
    'includes': INCLUDES,
    'excludes': EXCLUDES,
    'iconfile': iconfile,
    'plist': {'CFBundleDocumentTypes': [{'CFBundleTypeExtensions': EDIT_EXT,
                                         'CFBundleTypeName': 'Text File',
                                         'CFBundleTypeRole': 'Editor'}],
              'CFBundleIdentifier': 'org.spyder-ide',
              'CFBundleShortVersionString': spy_version}
}

if make_app:
    if make_alias:
        logger.info('Creating app bundle in alias mode...')
    else:
        logger.info('Creating app bundle...')
    setup(app=APP, options={'py2app': OPTIONS})
else:
    logger.info('Skipping app bundle...')

# =============================================================================
# Post App Creation
# =============================================================================
if make_app:
    _py_ver = f'python{py_ver[0]}.{py_ver[1]}'
    # copy egg info from site-packages: fixes pkg_resources issue for pyls
    for dist in pkg_resources.working_set:
        dest = os.path.join(distdir, MAC_APP_NAME, 'Contents', 'Resources',
                            'lib', _py_ver, os.path.basename(dist.egg_info))
        shutil.copytree(dist.egg_info, dest)

# =============================================================================
# DMG Creation
# =============================================================================
appfile = os.path.join(distdir, MAC_APP_NAME)
name = '{}-{} Py-{}.{}.{}'.format(MAC_APP_NAME[:-4], spy_version, *py_ver)
if make_lite:
    name += ' (lite)'
dmgfile = os.path.join(distdir, name + '.dmg')
settings_file = os.path.join(this_repo, 'dmg_settings.py')
defines = {'app': appfile, 'badge_icon': iconfile}

if make_dmg:
    logger.info('Building dmg file...')
    build_dmg(dmgfile, name, settings_file=settings_file, defines=defines)
else:
    logger.info('Skipping dmg file...')

# =============================================================================
# Clean Up
# =============================================================================
if not make_alias:
    logger.info('Cleaning up...')
    shutil.rmtree('spyder', ignore_errors=True)
    shutil.rmtree('spyder_kernels', ignore_errors=True)
    if os.path.exists(APP_MAIN_SCRIPT):
        os.remove(APP_MAIN_SCRIPT)
else:
    logger.info('Keeping "spyder" and "spyder_kernels" for alias mode')
