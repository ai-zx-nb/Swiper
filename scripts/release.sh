#!/bin/bash

LOCAL_DIR="./"
REMOTE_DIR="/opt/swiper/"

USER="ubuntu"
HOST="121.36.230.33"

# 上传代码
rsync -crvP --exclude={.git,.venv,logs,__pycache__} $LOCAL_DIR $USER@$HOST:$REMOTE_DIR

# 重启远程 Swiper 项目
read -p '是否要重启远程服务器? (y / n) ' restart

if [[ $restart == 'y' || $restart == 'Y' ]]; then
    exec /opt/swiper/scripts/restart.sh
else
    echo 'Bye'
fi
