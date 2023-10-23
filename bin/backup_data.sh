#!/bin/bash

today=`date +"%Y-%m-%d"`
backup_filepath=/data/backups/dla-${today}.tgz

cd /data
revver $backup_filepath

tar czvf $backup_filepath \
    --exclude='display' --exclude='thumb' --exclude='tiny' \
    --exclude='.git' --exclude='tmp' \
    dla
cd -


