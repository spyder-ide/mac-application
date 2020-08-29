#!/bin/bash
set -e

help()
{
    echo ""
    echo "create-build-env.sh [-h] [-v PYVER] ENV"
    echo "Create fresh pyenv environment ENV with Python version PYVER and install spyder"
    echo "dependents. Dependents are determined from the current spyder subrepo and"
    echo "python-language-server is installed from the subsubrepo"
    echo ""
    echo "Required:"
    echo "  ENV         Environment name"
    echo ""
    echo "Options:"
    echo "  -h          Display this help"
    echo "  -v PYVER    Specify the Python version. Default is 3.8.2"
    echo ""
}

PYVER=3.8.2
SUBREPO=./subrepos/spyder
PYLS=${SUBREPO}/external-deps/python-language-server
SPYK=${SUBREPO}/external-deps/spyder-kernels

while getopts "hv:" option; do
    case $option in
        h)
            help
            exit;;
        v)
            PYVER=$OPTARG;;
    esac
done
shift $(($OPTIND - 1))

ENV=$1

if [[ -z $ENV ]]; then
    echo "Please specify environment name."
    exit
fi
if [[ -n $CONDA_DEFAULT_ENV ]]; then
    echo "Please deactivate $CONDA_DEFAULT_ENV"
    exit
fi
if [[ -n $PYENV_VERSION && $PYENV_VERSION==$ENV ]]; then
    echo "Please deactivate $PYENV_VERSION"
    exit
fi

echo "Removing $ENV environment..."
pyenv uninstall -f $ENV

echo "Building $ENV environment..."
pyenv virtualenv $PYVER $ENV
export PYENV_VERSION=$ENV

pip install -U pip

echo "Installing spyder dependants..."
pip install -r req-build.txt -r req-extras.txt -c req-const.txt \
            -e ${PYLS} -e ${SPYK} -e ${SUBREPO}
pip uninstall -q -y spyder
