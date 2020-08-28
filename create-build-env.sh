#!/bin/bash

help()
{
    echo "create-build-env.sh [-h] [-a] [-e <ENV>] [-v <PYVER>]"
    echo "Create fresh pyenv environment ENV with Python version PYVER and install spyder"
    echo "dependents. Dependents are determined from the current spyder subrepo and"
    echo "python-language-server is installed from the subsubrepo"
    echo "Options:"
    echo "  -h          Display this help"
    echo "  -a          Force reinstall build and extras requirment files, and all spyder"
    echo "              dependents; otherwise only force reinstall python-language-server"
    echo "  -e ENV      Specify the environment name"
    echo "  -v PYVER    Specify the Python version. Default is 3.8.2"
}

PYVER=3.8.2
SUBREPO=./subrepos/spyder
PYLS=${SUBREPO}/external-deps/python-language-server

while getopts ":ae:hv:" option; do
    case $option in
        a)
        	ALL=1;;
        e)
            ENV=$OPTARG;;
        h)
            help
            exit;;
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

if [[ -n $ALL ]]; then
    echo 'Removing pyenv '$ENV' environment'
    pyenv uninstall -f $ENV

    echo 'Building '$ENV' environment'
    pyenv virtualenv $PYVER $ENV
    export PYENV_VERSION=$ENV

    pip install -U pip

    echo 'Installing all spyder dependants'
    pip install --force-reinstall\
        -r req-build.txt -r req-extras.txt -c req-const.txt -e ${PYLS} -e ${SUBREPO}
    pip uninstall -q -y spyder
else
    echo 'Installing PyLS and spyder-kernels'
    pip install --no-deps --force-reinstall -q -e ${PYLS}
fi
