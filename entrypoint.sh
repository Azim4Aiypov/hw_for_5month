#!/bin/bash
set -e

echo "⏳ Ждём базу данных..."
# Ждём пока PostgreSQL запустится
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "База данных недоступна - спим..."
  sleep 1
done
echo "✅ База данных доступна!"

# Применяем миграции
python manage.py migrate --noinput

# Собираем статические файлы (если нужно)
python manage.py collectstatic --noinput || true

echo "🚀 Запускаем сервер..."
exec "$@"
