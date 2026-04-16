"""Simple HTTP server for serving the frontend and lightweight API routes."""

from __future__ import annotations

import json
import signal
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from api.routes import get_api_response


BASE_DIR = Path(r"C:\anil")
FRONTEND_DIR = BASE_DIR / "frontend"
HOST = "0.0.0.0"
PORT = 8000


class DashboardRequestHandler(SimpleHTTPRequestHandler):
    """Serve static frontend files and JSON API responses."""

    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/api/"):
            payload, status_code = get_api_response(parsed_path.path)
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
            return

        if parsed_path.path in {"/", ""}:
            self.path = "/index.html"
        super().do_GET()


def main() -> None:
    """Start the dashboard server."""
    handler = partial(DashboardRequestHandler, directory=str(FRONTEND_DIR))
    httpd = HTTPServer((HOST, PORT), handler)

    def shutdown_server(_signum=None, _frame=None) -> None:
        print("\nShutting down server gracefully...")
        httpd.shutdown()

    signal.signal(signal.SIGINT, shutdown_server)

    print("Server running at http://localhost:8000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        shutdown_server()
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
