#!/usr/bin/env bash

export ENV=production

PIDS=`ps -ef | grep jtoa | grep -v grep | awk '{print $2}'`
for PID in $PIDS
do
    echo "kill $PID"
    kill -9 $PID
done
BUILD_ID=dontKillMe
pipenv run gunicorn -c gunicorn.conf.py main:app
echo "start success"