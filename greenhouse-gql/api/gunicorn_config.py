import os

PORT = os.environ.get("PORT", "8000")

bind = f"0.0.0.0:{PORT}"
# 2 - 4 x (NUM_CORES)
# AppEngine: https://cloud.google.com/appengine/docs/standard/python3/runtime
workers = os.environ.get("WEB_CONCURRENCY", 2)
print(f"using %s gunicorn workers {workers}")
timeout = 65
graceful_timeout = 65

# setting this to load api code before forking worker processes. This creates a faster boot
# time and causes errors during loading to be sent to stdout instead of being lost
preload_app = True

wsgi_app = "app:create_app()"
