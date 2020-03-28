#!/bin/bash

PROJECT_DIR='/opt/swiper'
LOG_FILE="$PROJECT_DIR/logs/celery.log"

cd $PROJECT_DIR
source .venv/bin/activate  # 加载虚拟环境
nohup celery worker -A task --loglevel=error > $LOG_FILE 2>&1 &
deactivate
cd -
echo 'Celery 启动完毕'
