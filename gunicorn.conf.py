# gunicorn config
import multiprocessing
from os import environ as env

PORT = 906
DEBUG_MODE = 1 if env.get('ENV') == 'development' else 0

# Gunicorn Configs
preload_app = True
worker_connections = 2000
bind = f'0.0.0.0:{PORT}'
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 * multiprocessing.cpu_count()

daemon = True
accesslog = 'logs/gunicorn_access.log'
access_log_format = "%(h)s %(r)s %(s)s %(a)s %(L)s"
errorlog = 'logs/gunicorn_error.log'
loglevel = 'debug'

capture_output = True
