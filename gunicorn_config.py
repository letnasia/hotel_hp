import os

# Bind
port = os.environ.get("PORT", 8000)
bind = f"0.0.0.0:{port}"

# Worker processes
workers = 2
worker_class = "sync"

# Threads per worker
threads = 1

# Logging
loglevel = "debug"

# Limit count of requests per worker
max_requests = 1000
