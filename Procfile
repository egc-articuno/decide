release: sh -c 'cd decide && python manage.py migrate'
web: sh -c 'cd decide && gunicorn --graceful-timeout=900 --timeout 900 decide.wsgi --log-file -'
