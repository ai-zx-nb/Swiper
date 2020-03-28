#!/bin/bash

PROJECT_DIR="/opt/swiper"
PID_FILE="$PROJECT_DIR/logs/gunicorn.pid"

if [ -f $PID_FILE ]; then
    PID=`cat $PID_FILE`
    kill $PID
    echo '进程已关闭'
else
    echo '进程未启动，无需关闭'
fi
