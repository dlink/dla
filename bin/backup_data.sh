#!/bin/bash

today=`date +"%Y-%m-%d"`
backup_filepath=/data/backups/dla/dla-${today}.tgz

cd /data
revver $backup_filepath

tar czvf $backup_filepath \
    --exclude='display' --exclude='thumb' --exclude='tiny' \
    --exclude='.git' --exclude='tmp' \
    dla
cd -
echo $backup_filepath created

