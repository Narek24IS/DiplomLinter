#!/bin/bash
set -e

echo "Запуск create_id_rsa.sh..."
sh /code/app/tools/create_id_rsa.sh

echo "Запуск tmp_cleanup.sh..."
sh /code/app/tools/tmp_cleanup.sh > /tmp/tmp_cleanup.log 2>&1 &

echo "Запуск веб-сервера:"
python3 /code/main.py