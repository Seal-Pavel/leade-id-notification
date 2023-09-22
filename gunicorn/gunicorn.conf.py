bind = '0.0.0.0:8080'
timeout = 99
accesslog = '-'
access_log_format = '[gunicorn] %a %t "%r" %s'
worker_class = 'aiohttp.GunicornWebWorker'
