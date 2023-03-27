#!/usr/bin/sh


chmod +x postinst

# build for linux ...
echo "[ BUILDING ] FOR LINUX ..."
termux-create-package manifast-linux.json


# build for termux ...
echo "[ BUILDING ] FOR TERMUX ..."
termux-create-package manifast-termux.json

