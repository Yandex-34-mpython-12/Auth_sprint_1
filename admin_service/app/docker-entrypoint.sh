#!/bin/sh

python manage.py collectstatic --noinput
uwsgi --strict --ini uwsgi.ini
