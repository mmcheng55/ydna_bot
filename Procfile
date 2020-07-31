worker: python main.py
web: gunicorn --worker-class quart.worker.GunicornWorker main_loop:app