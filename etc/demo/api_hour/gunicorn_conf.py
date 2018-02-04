import multiprocessing
import os

workers = multiprocessing.cpu_count() * 2
workers = 1  # dev mode

if os.environ.get('TRAVIS') == 'true':
    workers = 1

bind = ('0.0.0.0:8888', )
