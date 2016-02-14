import multiprocessing
import os

bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1

log_dir = "/tmp"
accesslog = os.path.join(log_dir, 'access.elevation.log')
errorlog = os.path.join(log_dir, 'error.elevation.log')
