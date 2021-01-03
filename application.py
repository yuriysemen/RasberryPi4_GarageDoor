"""
This file will be run by uwsgi
and loads the core application
and it's routes

Minimal modification should
be required
"""
from app import app as application

if __name__ == "__main__":
    application.run(host="0.0.0.0", port="5000")
