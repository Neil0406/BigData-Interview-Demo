#!/bin/sh
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
uwsgi --ini uwsgi.ini