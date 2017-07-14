#!/bin/bash
PYTHON_DIR=/usr/local/python

cd /skep/skep
# $PYTHON_DIR/bin/python manage.py syncdb --noinput
python manage.py syncdb --noinput
uwsgi --reload /skep/skep.pid
