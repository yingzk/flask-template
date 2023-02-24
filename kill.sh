#!/usr/bin/env bash

PIDS=`ps -ef | grep gunicorn | grep -v grep | awk '{print $2}'`
for PID in $PIDS
do
    echo "kill $PID"
    kill -9 $PID
done