#!/bin/bash
set -e

echo "Запуск create_id_rsa.sh..."
sh /src/app/tools/create_id_rsa.sh

echo "Запуск tmp_cleanup.sh..."
sh /src/app/tools/tmp_cleanup.sh > /tmp/tmp_cleanup.log 2>&1 &

echo "Запуск веб-сервера:"
python3 /src/main.py