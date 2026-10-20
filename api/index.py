import os
import sys

# Ensure project root directory is on sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app


class VercelPathFixMiddleware:
    """
    Middleware to recover the original request URI on Vercel.
    Vercel rewrites often set PATH_INFO to the destination (/api/index),
    while storing the actual client request URI in proxy headers.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        target_path = (
            environ.get("HTTP_X_FORWARDED_URI")
            or environ.get("HTTP_X_MATCHED_PATH")
            or environ.get("RAW_URI")
            or environ.get("REQUEST_URI")
        )
        if target_path:
            environ["PATH_INFO"] = target_path.split("?")[0]
        elif environ.get("PATH_INFO") == "/api/index":
            environ["PATH_INFO"] = "/"

        return self.wsgi_app(environ, start_response)


app.wsgi_app = VercelPathFixMiddleware(app.wsgi_app)
