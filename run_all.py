"""Project runner for the Sales Performance & Profit Analysis System."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


BASE_DIR = Path(r"C:\anil")
PYTHON_DIR = BASE_DIR / "python_analysis"
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
OUTPUT_CHARTS_DIR = PYTHON_DIR / "output_charts"
FRONTEND_IMAGES_DIR = FRONTEND_DIR / "images"

SCRIPT_SEQUENCE = [
    "01_generate_or_load_dataset.py",
    "02_data_cleaning.py",
    "03_data_analysis.py",
    "04_visualizations.py",
    "05_forecasting.py",
    "06_export_json_for_frontend.py",
]

REQUIRED_DIRECTORIES = [
    PYTHON_DIR,
    OUTPUT_CHARTS_DIR,
    BACKEND_DIR,
    BACKEND_DIR / "api",
    FRONTEND_DIR,
    FRONTEND_DIR / "css",
    FRONTEND_DIR / "js",
    FRONTEND_DIR / "pages",
    FRONTEND_IMAGES_DIR,
    BASE_DIR / "sql_scripts",
    BASE_DIR / "excel_dashboard",
    BASE_DIR / "powerbi",
    BASE_DIR / "project_report",
]


def configure_console() -> None:
    """Enable UTF-8 console output so status symbols print correctly."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def print_banner() -> None:
    """Print an ASCII welcome banner."""
    banner = r"""
+---------------------------------------------------------------+
|        Sales Performance & Profit Analysis System             |
+---------------------------------------------------------------+
"""
    print(banner)


def ensure_directories() -> None:
    """Create required directories when missing."""
    for directory in REQUIRED_DIRECTORIES:
        os.makedirs(directory, exist_ok=True)


def run_script(script_name: str) -> tuple[bool, float]:
    """Run a Python script and return success status with elapsed seconds."""
    script_path = PYTHON_DIR / script_name
    start_time = time.perf_counter()
    print(f"\nRunning {script_name} ...")

    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(BASE_DIR),
            check=True,
        )
        elapsed = time.perf_counter() - start_time
        print(f"✅ {script_name} completed in {elapsed:.2f}s")
        return True, elapsed
    except subprocess.CalledProcessError as exc:
        elapsed = time.perf_counter() - start_time
        print(f"❌ {script_name} failed in {elapsed:.2f}s (exit code {exc.returncode})")
        return False, elapsed
    except Exception as exc:  # pragma: no cover - defensive runtime safety
        elapsed = time.perf_counter() - start_time
        print(f"❌ {script_name} failed in {elapsed:.2f}s: {exc}")
        return False, elapsed


def copy_generated_charts() -> int:
    """Copy generated PNG charts into the frontend images folder."""
    FRONTEND_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    copied = 0

    for png_file in OUTPUT_CHARTS_DIR.glob("*.png"):
        destination = FRONTEND_IMAGES_DIR / png_file.name
        shutil.copy2(png_file, destination)
        copied += 1

    print(f"\nCopied {copied} PNG chart(s) to {FRONTEND_IMAGES_DIR}")
    return copied


def summarize_files() -> dict[str, int]:
    """Return a simple file count summary for key output folders."""
    summary = {
        "Base files": sum(1 for item in BASE_DIR.iterdir() if item.is_file()),
        "Python outputs": sum(1 for item in OUTPUT_CHARTS_DIR.glob("*") if item.is_file()),
        "Frontend assets": sum(1 for item in FRONTEND_IMAGES_DIR.glob("*") if item.is_file()),
        "Project documents": sum(
            1
            for item in [
                BASE_DIR / "cleaned_sales_data.csv",
                BASE_DIR / "analysis_results.txt",
                BASE_DIR / "excel_dashboard" / "Sales_Dashboard.xlsx",
                FRONTEND_DIR / "js" / "data.js",
            ]
            if item.exists()
        ),
    }
    return summary


def start_server() -> None:
    """Start the backend HTTP server in a background process."""
    server_path = BACKEND_DIR / "server.py"
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    subprocess.Popen(
        [sys.executable, str(server_path)],
        cwd=str(BASE_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    print("\nDashboard ready at http://localhost:8000")


def main() -> None:
    """Run the complete project pipeline."""
    configure_console()
    total_start = time.perf_counter()
    print_banner()
    ensure_directories()

    completed_steps = 0
    total_steps = len(SCRIPT_SEQUENCE)
    script_timings: list[tuple[str, float]] = []

    for script_name in SCRIPT_SEQUENCE:
        success, elapsed = run_script(script_name)
        script_timings.append((script_name, elapsed))
        if not success:
            print("\nPipeline stopped because a required step failed.")
            return
        completed_steps += 1

    copied_pngs = copy_generated_charts()
    total_elapsed = time.perf_counter() - total_start
    summary = summarize_files()

    print("\nExecution Summary")
    print("-" * 60)
    for script_name, elapsed in script_timings:
        print(f"{script_name:<35} {elapsed:>8.2f}s")
    print("-" * 60)
    print(f"Completed steps : {completed_steps}/{total_steps}")
    print(f"Copied PNGs     : {copied_pngs}")
    print(f"Total time      : {total_elapsed:.2f}s")
    for label, count in summary.items():
        print(f"{label:<16}: {count}")

    start_server()


if __name__ == "__main__":
    main()
