# Устанавливаем базовый образ с Python
FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    clang-format \
    golang \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Настраиваем рабочую директорию
WORKDIR /app
COPY . /app

# Делаем скрипт исполняемым
RUN chmod +x /app/src/main.py

ENTRYPOINT ["python", "/app/src/main.py"]