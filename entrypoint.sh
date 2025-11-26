#!/bin/sh
set -e

POSTGRES_HOST=${DB_HOST}
POSTGRES_PORT=${DB_PORT}

echo "⏳ Ждём базу данных..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "База данных недоступна - спим..."
  sleep 1
done
echo "✅ База данных доступна!"

echo "⏳ Ждём Redis..."
until nc -z "$REDIS_HOST" "$REDIS_PORT"; do
  echo "Redis недоступен - спим..."
  sleep 1
done
echo "✅ Redis доступен!"

if [ "$1" = "gunicorn" ]; then
    echo "🚀 Применяем миграции и собираем статику..."
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput || true
fi

echo "🚀 Запускаем сервис: $@"
exec "$@"
