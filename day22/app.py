from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os

VERSION = os.environ.get("APP_VERSION", "unknown")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({
            "version": VERSION,
            "healthy": True,
            "path": self.path
        }).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
