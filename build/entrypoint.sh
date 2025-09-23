#!/bin/sh

echo "Waiting for redis, nats..."

# until ping -c 1 redis && ping -c 1  nats
# do
#   sleep 0.5
# done

# echo "PostgreSQL started"

# python manage.py flush --no-input
# python manage.py collectstatic  --noinput
python manage.py migrate

# ./stream_scripts/create_streams.py 

exec "$@"
