#!/bin/bash

help()
{
    echo "spyder-subrepo.sh [-b <BRANCH>] [-h]"
    echo "Clone development spyder subrepo to subprepos directory and create symbolic link"
    echo "in current directory."
    echo "Options:"
    echo "  -b BRANCH   Checkout BRANCH of the spyder subrepo"
    echo "  -h          Display this help"
}
if [[ -n $CONDA_PREFIX ]]; then
    echo 'In conda environment; exiting'
    exit 1
fi

REPO=~/Documents/Python/spyder
SUBREPO=./subrepos/spyder

while getopts ":b:h" option; do
    case "$option" in
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
