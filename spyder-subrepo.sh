#!/bin/bash
set -e

if [[ -n $CONDA_PREFIX ]]; then
    echo 'In conda environment; exiting'
    exit 1
fi

REPO=../spyder
SUBREPO=./spyder-subrepo
PYLS=${SUBREPO}/external-deps/python-language-server
KERN=${SUBREPO}/external-deps/spyder-kernels

while [[ $# -gt 0 ]]; do
    case "$1" in
        -b)
            shift
            BRANCH=$1
            shift
            ;;
        --all)
            shift
            ALL=1
            ;;
        *)
            shift
            ;;
    esac
done

echo 'Cloning '${REPO}
git subrepo clone -f ${REPO} ${SUBREPO} -b ${BRANCH:?must specify branch: -b <BRANCH>}

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
