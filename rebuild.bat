mysql -u printer --password=printer01 printer < rebuild_database.sql
python manage.py syncdb --noinput
mysql -u printer --password=printer01 printer < loc.sql
pause
