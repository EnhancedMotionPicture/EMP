#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT / "apps" / "web-player")
server = ThreadingHTTPServer(("127.0.0.1", 8080), SimpleHTTPRequestHandler)
print("Serving web player at http://127.0.0.1:8080")
server.serve_forever()
