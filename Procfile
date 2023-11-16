web: gunicorn NeivaNet.wsgi --log-file -
web: gunicorn NeivaNet.wsgi
web: python manage.py collectstatic --noinput && gunicorn NeivaNet.wsgi
