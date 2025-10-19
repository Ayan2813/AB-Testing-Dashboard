# A/B Testing Dashboard

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Yes-brightgreen)
![MySQL](https://img.shields.io/badge/MySQL-Yes-orange)
![License](https://img.shields.io/github/license/Ayan2813/AB-Testing-Dashboard)

---

## **Overview**
The **A/B Testing Dashboard** is an interactive Streamlit application designed to help product managers, analysts, and data scientists **analyze A/B experiments** efficiently. It provides a **real-time view of experiment metrics**, allows **dynamic filtering**, and generates **exportable reports** to support data-driven decisions.

---

## **Key Features**
- **Data Integration:**  
  - Load experiment data directly from **MySQL** or upload a **CSV file**.
- **Dynamic Filters:**  
  - Filter by **Date Range, Device Type, Country, Traffic Source, and Groups**.
- **Metrics & Analysis:**  
  - Total Users, Conversions, Conversion Rate  
  - Uplift, Z-statistic, P-value  
  - Significance Indicator & Hypothesis Summary (e.g., “Variant B beats A”)
- **Visualizations:**  
  - Interactive bar charts showing **conversion rates by group**.
- **Export Options:**  
  - Download filtered data as **CSV**  
  - Export full experiment summary as **PDF** including metrics, hypothesis, and charts
- **Responsive UI:**  
  - Collapsible sidebar for filters and options  
  - Clean layout for metrics and charts  

---

## **Tech Stack**
- **Backend:** Python, MySQL  
- **Frontend:** Streamlit  
- **Data Analysis & Visualization:** pandas, statsmodels, seaborn, matplotlib  

---
