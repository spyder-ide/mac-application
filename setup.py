# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Create a stand-alone Mac OS X app using py2app

To be used like this:
$ python setup.py py2app

NOTES
-----
py2app includes all packages in Spyder.app/Contents/Resources/lib/python38.zip
but some packages have issues when placed there.
The following packages are included in py2app's PACKAGES option so that they
will be placed in Spyder.app/Contents/Resources/lib/python38 instead.

alabaster :
    Error message: [Errno 20] Not a directory: '<path>/Resources/lib/
    python38.zip/alabaster'
astroid :
    ImportError: cannot import name 'context' from 'astroid'
    (<path>/Resources/lib/python38.zip/astroid/__init__.pyc)
ipykernel :
    ModuleNotFoundError: No module named 'ipykernel.datapub'
ipython :
    [IPKernelApp] WARNING | Could not copy README_STARTUP to startup dir.
    Source file
    <path>/Resources/lib/python38.zip/IPython/core/profile/README_STARTUP
    does not exist
jedi :
    jedi.api.environment.InvalidPythonEnvironment: Could not get version
    information for '<path>/Contents/MacOS/python': InternalError("The
    subprocess <path>/Contents/MacOS/python has crashed (EOFError('Ran out
    of input'), stderr=).")
jinja2 :
    No module named 'jinja2.ext'
keyring :
    ModuleNotFoundError: No module named 'keyring.backends.<mod>'
parso :
    NotADirectoryError: [Errno 20] Not a directory:
    '<path>/Resources/lib/python38.zip/parso/python/grammar38.txt'
pygments :
    ModuleNotFoundError: No module named 'pygments.formatters.latex'
pyls :
    <path>/Contents/MacOS/python: No module named pyls
    Note: still occurs in alias mode
qtawesome :
    NotADirectoryError: [Errno 20] Not a directory: '<path>/Resourses/lib/
    python38.zip/qtawesome/fonts/fontawesome4.7-webfont.ttf'
spyder :
    NotADirectoryError: [Errno 20] Not a directory: '<path>/Resources/lib/
    python38.zip/spyder/app/mac_stylesheet.qss'
spyder_kernels :
    No module named spyder_kernels.console.__main__
sphinx :
    No module named 'sphinx.builders.changes'

"""

import os
import sys
import shutil
import pkg_resources
import subprocess as sp
from logging import getLogger, StreamHandler, Formatter
from setuptools import setup
from dmgbuild import build_dmg

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

# setup logger
fmt = Formatter('%(asctime)s [%(levelname)s] [%(name)s] -> %(message)s')
h = StreamHandler()
h.setFormatter(fmt)
logger = getLogger('Spy-Mac-App')
logger.addHandler(h)
logger.setLevel('INFO')

# setup paths
here = os.path.abspath(__file__)
this_repo = os.path.dirname(here)
basedir = os.path.dirname(this_repo)
distdir = os.path.join(this_repo, 'dist')
spy_repo = os.path.join(basedir, 'spyder')
deps_dir = os.path.join(spy_repo, 'external-deps')

# =============================================================================
# Copy Spyder Source to Repo
# =============================================================================
shutil.rmtree('spyder', ignore_errors=True)
shutil.copytree(os.path.join(spy_repo, 'spyder'), 'spyder')

# =============================================================================
# Install Python Language Server and Spyder Kernels from Subrepos
# =============================================================================
for pkg_name in ['python-language-server', 'spyder-kernels']:
    logger.info(f'Installing {pkg_name} from Spyder subrepo')
    pkg_dir = os.path.join(deps_dir, pkg_name)
    sp.check_output(['pip', 'install', '--no-deps', '--force-reinstall',
                     '-e', pkg_dir])

# =============================================================================
# App Creation
# =============================================================================
from spyder import __version__ as spy_version                    # noqa
from spyder.config.utils import EDIT_FILETYPES, _get_extensions  # noqa
from spyder.config.base import MAC_APP_NAME                      # noqa

iconfile = os.path.join(spy_repo, 'img_src', 'spyder.icns')

py_ver = [sys.version_info.major, sys.version_info.minor,
          sys.version_info.micro]

APP_MAIN_SCRIPT = MAC_APP_NAME[:-4] + '.py'
shutil.copy2(os.path.join(spy_repo, 'scripts', 'spyder'), APP_MAIN_SCRIPT)

APP = [APP_MAIN_SCRIPT]
PACKAGES = ['alabaster', 'astroid', 'ipykernel', 'IPython', 'jedi', 'jinja2',
            'keyring', 'parso', 'pygments', 'pyls', 'qtawesome', 'spyder',
            'spyder_kernels', 'sphinx',
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
        if dist.egg_info is None:
            continue
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
    if os.path.exists(APP_MAIN_SCRIPT):
        os.remove(APP_MAIN_SCRIPT)
else:
    logger.info('Keeping "spyder" for alias mode')
