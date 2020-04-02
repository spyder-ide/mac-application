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
base = os.path.dirname(this_repo)
dist = os.path.join(this_repo, 'dist')
spy_repo = os.path.join(base, 'spyder')
ker_repo = os.path.join(base, 'spyder-kernels')

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
make_dmg = False
if '--lite' in sys.argv:
    make_lite = True
    sys.argv.remove('--lite')
if '--no-dmg' in sys.argv:
    make_dmg = False
    sys.argv.remove('--no-dmg')

iconfile = os.path.join(spy_repo, 'img_src', 'spyder.icns')

#==============================================================================
# App Creation
#==============================================================================
APP_MAIN_SCRIPT = MAC_APP_NAME[:-4] + '.py'
shutil.copy2(os.path.join(spy_repo, 'scripts', 'spyder'), APP_MAIN_SCRIPT)

APP = [APP_MAIN_SCRIPT]
EXCLUDES = []
PACKAGES = [
            # Cannot be in Resources/lib/pythonXX.zip
            'astroid',         # ImportError: cannot import name 'context' from 'astroid' (<path>/Resources/lib/python38.zip/astroid/__init__.pyc)
            'pygments',        # ModuleNotFoundError: No module named 'pygments.formatters.latex'
            'qtawesome',       # NotADirectoryError: [Errno 20] Not a directory: '<path>/Resources/lib/python38.zip/qtawesome/fonts/fontawesome4.7-webfont.ttf'
            'spyder',          # NotADirectoryError: [Errno 20] Not a directory: '<path>/Resources/lib/python38.zip/spyder/app/mac_stylesheet.qss'
            'spyder_kernels',  # No module named spyder_kernels.console.__main__
            'ipykernel',       # ModuleNotFoundError: No module named 'ipykernel.datapub'
            # 'sphinx',
            # 'jinja2',
            # 'docutils',
            # 'alabaster',
            # 'babel',
            # 'snowballstemmer',
            # 'IPython',
            # 'ipython_genutils',
            # 'jupyter_client',
            # 'jupyter_core',
            # 'traitlets',
            # 'qtconsole',
            # 'pexpect',
            # 'jedi',
            # 'jsonschema',
            # 'nbconvert',
            # 'nbformat',
            # 'qtpy',
            # 'zmq',
            # 'distutils',
            # 'PyQt5',
            # 'psutil',
            # 'wrapt',
            # 'lazy_object_proxy',
            # 'pyls',
            # 'pylint',
            # 'pycodestyle',
            # 'pyflakes',
            # 'autopep8',
            # 'flake8',
            ]

if make_lite:
    INCLUDES = []
else:
    INCLUDES = ['numpy', 'scipy', 'pandas', 'matplotlib', 'cython', 'sympy']

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
# DMG Creation
# =============================================================================
py_version = sys.version.split(' ')[0]

appfile = os.path.join(dist, MAC_APP_NAME)
name = f'{MAC_APP_NAME[:-4]}-{spy_version} Py-{py_version}'
dmgfile = os.path.join(dist, f'{name}.dmg')
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
