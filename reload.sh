#!/bin/bash
PYTHON_DIR=/usr/local/python

cd /printer/printer
# $PYTHON_DIR/bin/python manage.py syncdb --noinput
python manage.py syncdb --noinput
uwsgi --reload /printer/printer.pid
