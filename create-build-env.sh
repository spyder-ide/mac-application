#!/bin/bash

help()
{
    echo "create-build-env.sh [-h][-e <ENV>][-v <PYVER>]"
    echo "Create fresh pyenv environment ENV with Python version PYVER"
    echo "Options:"
    echo "  -h          Display this help"
    echo "  -e ENV      Specify the environment name"
    echo "  -v PYVER    Specify the Python version. Default is 3.8.2"
}

PYVER=3.8.2

while getopts ":e:h" option; do
    case $option in
        h)
            help
            exit;;
        e)
            ENV=$OPTARG;;
        v)
            PYVER=$OPTARG;;
        *)
            echo "Invalid option"
            exit;;
    esac
done
shift $(($OPTIND - 1))

if [[ -z $ENV ]]; then
    echo "Must specify environment name: -e <ENV>"
    exit
fi

echo 'Removing pyenv '$ENV' environment'
pyenv uninstall -f $ENV

echo 'Building '$ENV' environment'
pyenv virtualenv $PYVER $ENV
export PYENV_VERSION=$ENV

pip install -U pip
