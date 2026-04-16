"""Helper functions for optional dashboard API endpoints."""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(r"C:\anil")
DATA_JS_FILE = BASE_DIR / "frontend" / "js" / "data.js"


def load_dashboard_data() -> dict:
    """Read dashboardData from the generated JavaScript file."""
    if not DATA_JS_FILE.exists():
        return {"error": "frontend/js/data.js has not been generated yet."}

    content = DATA_JS_FILE.read_text(encoding="utf-8").strip()
    prefix = "window.dashboardData = "
    if not content.startswith(prefix):
        return {"error": "data.js is not in the expected format."}

    json_payload = content[len(prefix):].rstrip().rstrip(";")
    return json.loads(json_payload)


def get_api_response(path: str) -> tuple[dict | list, int]:
    """Return payload and status code for supported API routes."""
    data = load_dashboard_data()
    if "error" in data:
        return data, 500

    routes = {
        "/api/kpis": data.get("overallKPIs", {}),
        "/api/sales/monthly": data.get("monthlySales", []),
        "/api/sales/regional": data.get("regionData", []),
        "/api/products/top": data.get("topProducts", []),
    }

    if path in routes:
        return routes[path], 200
    return {"error": f"Route not found: {path}"}, 404
