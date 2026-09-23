# 🍔 Fast Food Marketing Campaign: End-to-End A/B Testing & BI Portfolio

[![Python](https://img.shields.io/badge/Python-Data_Science-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Excel](https://img.shields.io/badge/Excel-Pivot_Analysis-217346.svg?logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/excel)
[![SQL](https://img.shields.io/badge/SQL-Advanced_Queries-4479A1.svg?logo=postgresql&logoColor=white)]()

## 🎯 Project Overview

A fast-food chain recently launched a new product and tested **three different promotional campaigns** across various market sizes (Small, Medium, Large) over a four-week period. The executive team needs a definitive answer: **Which promotion drives the most sales, and which one should be rolled out nationwide?**

This project provides an end-to-end analytical solution. Moving beyond basic averages, it leverages rigorous statistical A/B Testing (ANOVA & Tukey HSD) alongside highly interactive Business Intelligence (BI) tools to ensure the final business recommendation is backed by mathematically significant evidence.

---

## 🛠️ Tech Stack

| Tool | Purpose | Key Techniques Applied |
|------|---------|------------------------|
| **Python** 🐍 | Statistical Analysis | `pandas`, `scipy.stats`, `statsmodels` |
| **Streamlit** 🌐 | Web Application | Interactive web dashboard, dynamic KPIs, layout caching |
| **Excel** 📗 | Exploratory Dashboards | Pivot Tables, Connected Slicers, Conditional Formatting |
| **SQL** 🗄️ | Data Querying | Aggregations, CTEs (Common Table Expressions), Window Functions |
| **Power BI** 📊 | Enterprise BI | Power Query (ETL), DAX, Star Schema Modeling |

---

## 💡 Key Features by Tool

*   **📗 Excel (`2_Excel/`)**: Built an interactive dashboard completely from scratch using the raw data. Features **5 interactive Pivot Tables** and Slicers utilizing **Report Connections** to cross-filter all charts simultaneously.
*   **🗄️ SQL (`3_SQL/`)**: Wrote advanced queries utilizing **CTEs** for age-tier bucketing and **Window Functions** (`RANK()`) to identify top-performing locations dynamically.
*   **📊 Power BI (`4_BI/`)**: Engineered a complete reporting solution. Handled **full ETL via Power Query** to clean the raw data and build a **Star Schema** (Fact & Dimension tables) entirely from scratch. Features robust **DAX measures** (e.g., dynamic `% Lift vs Baseline` using `VAR` and `REMOVEFILTERS`), Interactive Tooltips, and Drill-through pages.
*   **🐍 Python (Jupyter Notebook) (`5_Python/`)**: Conducted rigorous statistical testing. Included assumption checks (**Shapiro-Wilk** for normality, **Levene** for equal variance), **One-Way ANOVA**, and **Tukey HSD Post-Hoc** analysis. The notebook explanations are uniquely **code-switched in Egyptian Arabic and English technical terms** to simulate a real-world Cairo tech team environment.
*   **🌐 Python (Streamlit) (`5_Python/`)**: Deployed the statistical findings into an interactive, user-friendly Streamlit web app, complete with dynamic visualization tabs and dynamic alpha-value sliders for significance testing.

---

## 📁 Project Structure

*Note: A core philosophy of this project is raw-data-first. The Excel and Power BI workflows both initiate directly from `dataset_raw.csv`, handling all data cleaning, transformations, and dimensional modeling (Star Schema) internally without relying on pre-processed CSVs.*

```text
Marketing_Campaign_AB_Test/
│
├── 1_Datasets/
│   ├── dataset_raw.csv                 # The raw, unprocessed source data
│   └── dataset_cleaned.csv             # Cleaned dataset (used for Python/SQL)
│
├── 2_Excel/
│   ├── Marketing_AB_Test_Excel.xlsx    # Full dashboard (Raw -> Pivot -> Dashboard)
│   └── Excel_Development_Guide.md      # Step-by-step Pivot Table/Slicer tutorial
│
├── 3_SQL/
│   ├── AB_Test_Queries.sql             # Aggregations, CTEs, and Window Functions
│   └── SQL_Development_Guide.md        # Query logic and business context
│
├── 4_BI/
│   ├── Power_BI_Dashboard.pbix         # End-to-end BI file (Power Query ETL + DAX)
│   └── BI_Development_Guide.md         # Guide on building the Star Schema & DAX
│
├── 5_Python/
│   ├── AB_Testing_Analysis.ipynb       # ANOVA & Tukey HSD (Egyptian Arabic/English)
│   ├── streamlit_app.py                # Interactive web dashboard application
│   └── stat_results/
│       └── tukey_results.json          # Cached statistical results for Streamlit
│
├── README.md                           # Project documentation (You are here)
└── requirements.txt                    # Python dependencies
```

---

## 📈 Executive Summary & Key Findings

After rigorous statistical testing, the results clearly dictate the next steps for the marketing team:

1.  **Stop Promotion 2 Immediately:** The data proves with statistical significance that Promotion 2 is the worst-performing campaign across all market sizes. Any budget allocated here is being wasted.
2.  **Promotions 1 & 3 are Winners:** Both campaigns heavily outperformed Promotion 2. 
3.  **The Tie-Breaker:** The difference in sales between Promo 1 and Promo 3 is **Statistically Insignificant** ($p > 0.05$). Because they perform equally well in terms of revenue, the final executive choice should be driven by secondary factors:
    *   Which campaign has a lower operational **cost**?
    *   Which campaign aligns better with long-term **brand strategy**?

---

## 🚀 How to Run & Use This Project

This project is built to be modular. You can review any specific track (Python, BI, SQL, Excel) independently.

### 🌐 1. Run the Streamlit Dashboard (Python)
To view the interactive web app locally:
1. Open your terminal and navigate to the project root.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run 5_Python/streamlit_app.py`

### 📊 2. Explore the Power BI Dashboard
1. Ensure you have [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installed.
2. Open `4_BI/Power_BI_Dashboard.pbix`.
3. Try interacting with the Slicers, hover over the Bar charts to see the custom Tooltips, and right-click on the Market Size donut chart to test the **Drill-through** feature.

### 📗 3. View the Excel Dashboard
1. Open `2_Excel/Marketing_AB_Test_Excel.xlsx`.
2. Navigate to the **Dashboard** sheet to test the slicers (which utilize Report Connections to update all 5 pivots instantly).

### 📓 4. Read the Jupyter Notebook
1. Open `5_Python/AB_Testing_Analysis.ipynb` in your preferred notebook editor.
2. Enjoy the code-switched technical walkthrough!

---
*Created as part of an Advanced Data Engineering & Analytics Portfolio.*
