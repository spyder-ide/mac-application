#!/bin/bash

# Copyright (c) 2014 - The Spyder Development team
# Distributed under the terms of the MIT license

# This script is based in this post
# http://securityandthe.net/2008/12/04/creating-compressed-dmg-files/

# Grabbing options
for i in "$@"
do
    case $i in
        --app=*)
            APP_PATH="${i#*=}"
            shift
            ;;
        --name=*)
            DMG_NAME="${i#*=}"
            shift
            ;;
        -h|--help)
            echo "Bash script to build a DMG file for Spyder"
	    echo ""
	    echo "Options:"
            echo "--app= : Path where Spyder.app is located (absolute or relative)"
            echo "--name= : Name to give to the DMG (e.g. spyder-x.y.z.dmg)"
	    exit
            ;;
        *)
          echo "Unknown option"
	  exit
          ;;
    esac
done

# Check if user has passed the needed command line args
if [ -z "$APP_PATH" ]; then
    echo "You need to pass the path where Spyder.app is located"
    exit
fi

if [ -z "$DMG_NAME" ]; then
    echo "You need to pass a name for the DMG"
    exit
fi

# Global variables
if [[ "$DMG_NAME" == *"py2.7"* ]]
then
    VOLNAME="Spyder-Py2";
else
    VOLNAME="Spyder";
fi

SIZE="600M"

# Ask for sudo before starting to avoid an error while creating
# the template
sudo echo "Starting"

# Removing possible stale files and dirs
rm -f *.dmg
sudo rm -Rf /Volumes/Spyder

# Creating template
echo ""
echo "Creating uncompressed disk image"
hdiutil create -size $SIZE -fs HFS+J -volname $VOLNAME ./template.dmg

# Mounting template
echo ""
echo "Mounting uncompressed disk image"
hdiutil attach template.dmg -readwrite -mount required

# Copy installer interface
echo ""
echo "Copying files"
mkdir -p /Volumes/Spyder/.background
cd files
cp -f background.png Chromium\ license.txt /Volumes/Spyder/.background/
cp -f DS_Store /Volumes/Spyder/.DS_Store
cp -f Applications /Volumes/Spyder/
cd ..

# Copy application
sudo rm -Rf /Volumes/Spyder/Spyder.app
cp -R $APP_PATH /Volumes/Spyder/

# Removing unneeded files
sudo rm -R /Volumes/Spyder/.Trashes
sudo rm -R /Volumes/Spyder/.fseventsd

# Unmounting template
echo ""
echo "Unmounting uncompressed image"
hdiutil detach /Volumes/$VOLNAME

# Compressing final image
echo ""
echo "Creating compressed image"
hdiutil convert template.dmg -format UDZO -imagekey zlib-level=9 -o $DMG_NAME

# Removing template
rm ./template.dmg
