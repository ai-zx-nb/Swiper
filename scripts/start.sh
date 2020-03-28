#!/bin/bash

PROJECT_DIR="/opt/swiper"

cd $PROJECT_DIR
source .venv/bin/activate  # 加载虚拟环境
gunicorn -c swiper/gconfig.py swiper.wsgi
deactivate
cd -
echo '启动完毕'
