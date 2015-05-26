# -*- coding: utf-8 -*-
"""
Symlink External Qt in Homebrew
"""

from __future__ import print_function

import os
import os.path as osp
import subprocess

# Getting the directory where we're going to symlink Qt
QT_VERSION = "4.8.6"
CELLAR = 'HOMEBREW_CELLAR'

brew_config = subprocess.check_output(['brew', '--config']).decode('utf-8')
brew_config = brew_config.split('\n')
cellar_config = [c for c in brew_config if c.startswith(CELLAR)][0]
cellar_dir = cellar_config.split()[1]
brew_qt_dir = osp.join(cellar_dir, 'qt', QT_VERSION)


# Creating the Homebrew Qt dir
try:
    os.makedirs(brew_qt_dir)
    os.chdir(brew_qt_dir)
except:
    print("Error creating Qt dir under Homebrew")


# Symlink the external Qt installation under the previous directory
try:
    os.symlink('/Developer/Tools/Qt', './bin')
    os.symlink('/Library/Frameworks', './Frameworks')
    os.symlink('/Developer/Applications/Qt/imports', './imports')
    os.symlink('/usr/local/Qt4.8/mkspecs', './mkspecs')
    os.symlink('/Developer/Applications/Qt/phrasebooks', './phrasebooks')
    os.symlink('/Developer/Applications/Qt/plugins/', './plugins')
    os.symlink('/Developer/Applications/Qt/translations', './translations')
except:
    print("Error creating symlinks")
