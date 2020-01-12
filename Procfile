% prepara el repositorio para su despliegue. 
release: sh -c 'cd decide && cp local_settings.heroku.py local_settings.py && python manage.py migrate'
% especifica el comando para lanzar Decide
web: sh -c 'cd decide && gunicorn --graceful-timeout=900 --timeout 900 decide.wsgi --log-file -'
