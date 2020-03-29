#!/bin/bash

PROJECT_DIR="/opt/swiper"
PID_FILE="$PROJECT_DIR/logs/gunicorn.pid"

if [ -f $PID_FILE ]; then
    echo '正在重启'
    PID=`cat $PID_FILE`
    kill -HUP $PID
    echo '重启完毕'
else
    echo '未找到 PID 文件，直接调用启动脚本'
    exec $PROJECT_DIR/scripts/start.sh
fi
