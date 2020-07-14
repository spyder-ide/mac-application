#!/bin/bash

help()
{
    echo "spyder-subrepo.sh [-a][-b <BRANCH>][-h]"
    echo "Clone development spyder subrepo and install python-language-server and spyder-kernels"
    echo "subrepos"
    echo "Options:"
    echo "  -a          Force reinstall build and extras requirment files, and all spyder dependents;"
    echo "              otherwise only force reinstall python-language-server and spyder-kernel"
    echo "              subprepos"
    echo "  -b BRANCH   Checkout BRANCH of the spyder subrepo"
    echo "  -h          Display this help"
}
if [[ -n $CONDA_PREFIX ]]; then
    echo 'In conda environment; exiting'
    exit 1
fi

REPO=~/Documents/Python/spyder
SUBREPO=./subrepos/spyder
PYLS=${SUBREPO}/external-deps/python-language-server
KERN=${SUBREPO}/external-deps/spyder-kernels

while getopts ":ab:h" option; do
    case "$option" in
        a)
            ALL=1;;
        b)
            BRANCH=$OPTARG;;
        h)
            help
            exit;;
        *)
            echo "Invalid option"
            exit;;
    esac
done
shift $(($OPTIND - 1))

if [[ -z $BRANCH ]]; then
    echo "Must specify branch: -b <BRANCH>"
    exit
fi

echo 'Cloning '${REPO}
git subrepo clone -f ${REPO} ${SUBREPO} -b ${BRANCH}

ln -sF "${SUBREPO}/spyder" .

if [[ -n $ALL ]]; then
    echo 'Installing all spyder dependants'
    pip install --force-reinstall\
        -r req-build.txt -r req-extras.txt -c req-const.txt -e ${PYLS} -e ${KERN} -e ${SUBREPO}
    pip uninstall -q -y spyder
else
    echo 'Installing PyLS and spyder-kernels'
    pip install --no-deps --force-reinstall -q -e ${PYLS} -e ${KERN}
fi
