import os

bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = 4
threads = 2
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"
