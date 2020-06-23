#!/bin/bash
set -e

while [[ $# -gt 0 ]]; do
    case "$1" in
        -e)
            shift
            ENV=$1
            shift
            ;;
        *)
            shift
            ;;
    esac
done

[[ ${ENV:?must specify environment name: -e <ENV>} ]]

echo 'Removing pyenv '$ENV' environment'
pyenv uninstall -f $ENV

echo 'Building '$ENV' environment'
pyenv virtualenv 3.8.2 $ENV
export PYENV_VERSION=$ENV

pip install -U pip
