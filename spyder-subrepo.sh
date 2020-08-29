#!/bin/bash
set -e

help()
{
    echo ""
    echo "spyder-subrepo.sh [-h] [-d REPO] [-b <BRANCH>]"
    echo "Clone spyder subrepo to subprepos directory and create symbolic link in current"
    echo "directory."
    echo ""
    echo "Options:"
    echo "  -d REPO     Repository to clone. Default https://github.com/spyder-ide/spyder.git"
    echo "  -b BRANCH   Checkout BRANCH of the spyder subrepo. Default is 4.x"
    echo "  -h          Display this help"
    echo ""
}

if [[ -n $CONDA_DEFAULT_ENV ]]; then
    echo "In conda environment; exiting"
    exit
fi

CLONE=https://github.com/spyder-ide/spyder.git
BRANCH=4.x
SUBREPO=./subrepos/spyder

while getopts "d:b:h" option; do
    case "$option" in
        d)
            CLONE=$OPTARG;;
        b)
            BRANCH=$OPTARG;;
        h)
            help
            exit;;
    esac
done
shift $(($OPTIND - 1))

echo "Cloning ${CLONE}"
git subrepo clone -f ${CLONE} ${SUBREPO} -b ${BRANCH}

ln -sF "${SUBREPO}/spyder" .
