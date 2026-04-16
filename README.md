# 📊 Sales Performance & Profit Analysis System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Excel](https://img.shields.io/badge/Excel-Dashboard-green)
![PowerBI](https://img.shields.io/badge/Power%20BI-Reporting-yellow)
![Frontend](https://img.shields.io/badge/HTML%2FCSS%2FJS-Chart.js-red)

This project is a complete sales analytics solution built around a real CSV dataset stored in `C:\anil`. It covers Python-based cleaning and analysis, MySQL-ready SQL scripts, an Excel dashboard, Power BI guidance, and a responsive frontend dashboard powered by `Chart.js`.

## Features
- Reads the existing CSV dataset from `C:\anil` without generating fake data.
- Cleans and enriches the dataset with margin, shipping, and time-based fields.
- Generates KPI summaries, formatted text analysis, and 16 PNG charts.
- Exports dashboard-ready JavaScript data for a static frontend.
- Creates an Excel workbook with formatted data and summary sheets.
- Includes MySQL 8.0 scripts, Power BI measures, theme configuration, and a full project report.
- Starts a local dashboard server at `http://localhost:8000`.

## Folder Tree
```text
C:\anil\
├── dataset.csv
├── generated_sales_data.csv
├── cleaned_sales_data.csv
├── analysis_results.txt
├── run_all.py
├── README.md
├── python_analysis\
│   ├── requirements.txt
│   ├── 01_generate_or_load_dataset.py
│   ├── 02_data_cleaning.py
│   ├── 03_data_analysis.py
│   ├── 04_visualizations.py
│   ├── 05_forecasting.py
│   ├── 06_export_json_for_frontend.py
│   └── output_charts\
├── sql_scripts\
├── excel_dashboard\
├── powerbi\
├── project_report\
├── frontend\
└── backend\
```

## Setup
1. Install Python dependencies:
   `pip install -r C:\anil\python_analysis\requirements.txt`
2. Run the complete pipeline:
   `python C:\anil\run_all.py`
3. Open the dashboard:
   [http://localhost:8000](http://localhost:8000)

## Technologies
| Technology | Purpose |
| --- | --- |
| Python | Data loading, cleaning, analytics, forecasting, Excel export |
| Pandas / NumPy | Data transformation and summary calculations |
| Matplotlib / Seaborn | Static chart generation |
| Scikit-learn | Linear regression forecasting |
| MySQL 8.0 | Database schema, inserts, analytical queries, procedures |
| Excel / openpyxl | Workbook creation and dashboard preparation |
| Power BI | Interactive BI reporting |
| HTML / CSS / JavaScript | Static frontend dashboard |
| Chart.js | Browser-based charts |
| Python `http.server` | Local dashboard hosting |

## Author
- Student Name: `____________________`
- Course: `BCA`
- Academic Session: `2024-25`
