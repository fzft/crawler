celery -A tasks flower --port=5555 >/dev/null 2>&1&
celery -A tasks worker -Q  yys --loglevel=info