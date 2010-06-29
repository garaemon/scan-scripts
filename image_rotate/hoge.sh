#!/bin/sh

DIR="$HOME/Dropbox/scan/minamike"
files=`find $DIR -name "*jpg"`
for f in $files
do
    echo $f
    ./image_rotate $f
done