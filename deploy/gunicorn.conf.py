import multiprocessing
import os

bind = "0.0.0.0:8282"
workers = multiprocessing.cpu_count() * 2 + 1

log_dir = "/var/elevation/logs"
accesslog = os.path.join(log_dir, 'access.gunicorn.elevation.log')
errorlog = os.path.join(log_dir, 'error.gunicorn.elevation.log')
