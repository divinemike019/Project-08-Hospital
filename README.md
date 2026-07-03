# Project 08 Hospital

**Dataset:** Hospital Admissions Data - Ashish Sahani  
**Source:** https://www.kaggle.com/datasets/ashishsahani/hospital-admissions-data  
**Author:** Charlie | TheBuild Data Analysis Programme | June 2026  
**Tools:** MySQL Workbench · Python 3 · Microsoft Excel

---

## Key Finding

Oncology has 31.2% readmission rate — highest of all departments. Winter admissions are 23% above summer baseline. Emergency handles 38% of all admissions.

---

## Files

| File | Purpose |
|------|---------|
| `sql/p8_hospital_analysis.sql` | MySQL schema + all analysis queries |
| `python/p8_hospital_analysis.py` | Data cleaning, feature engineering, charts |
| `excel/P8_Hospital_Dashboard.xlsx` | Interactive Excel dashboard with charts |

## Folder Structure

```
Project_08_Hospital/
├── sql/
│   └── p8_hospital_analysis.sql
├── python/
│   └── p8_hospital_analysis.py
├── excel/
│   └── P8_Hospital_Dashboard.xlsx
├── data/          ← place your CSV files here (not committed)
└── outputs/
    └── charts/    ← Python charts saved here
```

## How to Run

```bash
# 1. Download dataset from URL above and place CSVs in data/
# 2. In MySQL Workbench: open and run the SQL file
# 3. Install Python dependencies
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
# 4. Run the Python script
python python/p8_hospital_analysis.py
# 5. Open the Excel file for the interactive dashboard
```

---
*TheBuild Data Analysis Programme · June 2026*
