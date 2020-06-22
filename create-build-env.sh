#!/bin/bash

if [[ $# -ge 1 && -n $1 ]]; then
    ENV=$1
else
    ENV=spy-build
fi

echo 'Removing pyenv '$ENV' environment'
pyenv uninstall -f $ENV

echo 'Building '$ENV' environment'
pyenv virtualenv 3.8.2 $ENV
export PYENV_VERSION=$ENV

echo 'Installing Spyder dependants'
pip install -r req-build.txt -r req-user.txt -c constraints.txt ../spyder
pip uninstall -y spyder

echo 'Copy Spyder to this repo'
cp -a ../spyder .

echo 'Removing pyls & spyder-kernels'
pip uninstall -q -y python-language-server spyder-kernels

echo 'Installing pyls from subrepo'
pip install --no-deps -q -e ./spyder/external-deps/python-language-server

echo 'Installing spyder-kernels from subrepo'
pip install --no-deps -q -e ./spyder/external-deps/spyder-kernels
