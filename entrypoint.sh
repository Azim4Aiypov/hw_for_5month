
set -e

echo "⏳ Ждём базу данных..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "База данных недоступна - спим..."
  sleep 1
done
echo "✅ База данных доступна!"

python manage.py migrate --noinput

python manage.py collectstatic --noinput || true

echo "🚀 Запускаем сервер..."
exec "$@"
