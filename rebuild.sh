#!/bin/bash
mysql -u skep --password=weizoom skep < rebuild_database.sql
python manage.py syncdb --noinput
mysql -u skep --password=weizoom skep < loc.sql
