#!/bin/sh
set -e

# Проверяем, был ли передан аргумент
if [ -n "$1" ]; then
  PRIVATE_KEY="$1"
  echo "Используется переданный аргумент как приватный ключ."
elif [ -n "${PRIVATE_KEY}" ]; then
  echo "Используется переменная окружения PRIVATE_KEY."
else
  echo "Ошибка: Не передан аргумент и не задана переменная окружения PRIVATE_KEY."
fi

# Проверяем, что ключ не пустой
if [ -z "${PRIVATE_KEY}" ]; then
  echo "Ошибка: Приватный ключ пустой."
else
  echo "${PRIVATE_KEY}" | sed 's/-----BEGIN OPENSSH PRIVATE KEY-----\(.*\)-----END OPENSSH PRIVATE KEY-----/\1/;s/ /\n/g;s/\(.*\)/-----BEGIN OPENSSH PRIVATE KEY-----\n\1\n-----END OPENSSH PRIVATE KEY-----/' > "${TMP_VOLUME_SSH}"/id_rsa
  chmod 0400 "${TMP_VOLUME_SSH}"/id_rsa

  echo "Приватный ключ успешно записан в ${TMP_VOLUME_SSH}/id_rsa"
fi
