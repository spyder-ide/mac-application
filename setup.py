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
from logging import getLogger
from setuptools import setup
from dmgbuild import build_dmg

logger = getLogger('Spy-Mac-App')

if not os.path.exists('spyder'):
    os.symlink('../spyder/spyder', 'spyder')
if not os.path.exists('spyder_kernels'):
    os.symlink('../spyder-kernels/spyder_kernels', 'spyder_kernels')

# here = os.path.abspath(__file__)
# basedir = os.path.dirname(os.path.dirname(here))
# spy_repo = os.path.join(basedir, 'spyder')
# ker_repo = os.path.join(basedir, 'spyder-kernels')
# # sys.path = [spy_repo, ker_repo] + sys.path
# sys.path = [spy_repo] + sys.path

from spyder import __version__ as spy_version
from spyder.config.utils import EDIT_FILETYPES, _get_extensions
from spyder.config.base import MAC_APP_NAME

here = os.path.realpath(__file__)
repodir = os.path.dirname(here)
distdir = os.path.join(repodir, 'dist')
spyrepo = os.path.realpath('../spyder')

iconfile = os.path.join(spyrepo, 'img_src', 'spyder.icns')

#==============================================================================
# App Creation
#==============================================================================
logger.info('Creating app bundle...')

APP_MAIN_SCRIPT = MAC_APP_NAME[:-4] + '.py'
# shutil.copyfile('../spyder/scripts/spyder', APP_MAIN_SCRIPT)
if not os.path.exists(APP_MAIN_SCRIPT):
    os.symlink(os.path.join(spyrepo, 'scripts', 'spyder'), APP_MAIN_SCRIPT)

APP = [APP_MAIN_SCRIPT]
EXCLUDES = []
PACKAGES = ['spyder', 'sphinx', 'jinja2', 'docutils', 'alabaster', 'babel',
            'snowballstemmer', 'IPython', 'ipykernel', 'ipython_genutils',
            'jupyter_client', 'jupyter_core', 'traitlets', 'qtconsole',
            'pexpect', 'jedi', 'jsonschema', 'nbconvert', 'nbformat', 'qtpy',
            'qtawesome', 'zmq', 'pygments', 'distutils', 'PyQt5', 'psutil',
            'wrapt', 'lazy_object_proxy', 'spyder_kernels', 'pyls',
            'pylint', 'astroid', 'pycodestyle', 'pyflakes']

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

setup(app=APP, options={'py2app': OPTIONS})

# =============================================================================
# DMG Creation
# =============================================================================
logger.info('Building dmg file...')

py_version = sys.version.split(' ')[0]

appfile = os.path.join(distdir, MAC_APP_NAME)
name = f'{MAC_APP_NAME[:-4]}-{spy_version} Py-{py_version}'
dmgfile = os.path.join(distdir, f'{name}.dmg')
settings_file = os.path.join(repodir, 'dmg_settings.py')
background = os.path.join(repodir, 'files', 'background.png')
defines = {'app': appfile, 'badge_icon': iconfile, 'background': background}
build_dmg(dmgfile, name, settings_file=settings_file, defines=defines)

# =============================================================================
# Clean Up
# =============================================================================
logger.info('Cleaning up build')

if os.path.exists('spyder'):
    os.remove('spyder')
if os.path.exists('spyder_kernels'):
    os.remove('spyder_kernels')
if os.path.exists(APP_MAIN_SCRIPT):
    os.remove(APP_MAIN_SCRIPT)
