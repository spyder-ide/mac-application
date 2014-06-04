# -*- coding: utf-8 -*-
"""
Symlink External Qt in Homebrew
"""

import os
import os.path as osp
import subprocess

QT_VERSION = "4.9.9"
CELLAR = 'HOMEBREW_CELLAR'

brew_config = subprocess.check_output(['brew', '--config']).split('\n')
cellar_config = [c for c in brew_config if c.startswith(CELLAR)][0]
cellar_dir = cellar_config.split()[1]

try:
    os.makedirs(osp.join(cellar_dir, QT_VERSION, 'Frameworks'))
except:
    pass