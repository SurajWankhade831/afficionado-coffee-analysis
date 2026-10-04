# Afficionado Coffee Roasters – Sales Trend and Time-Based Performance Analysis

## 📌 Project Overview

This project analyzes transaction-level sales data from **Afficionado Coffee Roasters** to understand sales performance, customer demand patterns, store performance, and product performance.

The analysis focuses mainly on **hourly sales trends**, because the dataset contains transaction time but does not contain an actual transaction date.

The objective is to convert raw transaction data into useful business insights that can support better staffing, inventory planning, and operational decisions.

---

## 🎯 Problem Statement

Afficionado Coffee Roasters has transaction-level sales data but needs a consolidated view of its sales performance.

Without structured analysis, it can be difficult to identify:

- High-demand hours
- Low-demand hours
- Store-level revenue differences
- Best-performing product categories
- High-demand product types
- Opportunities for better staffing and inventory planning

This project uses Python and data analysis techniques to identify these patterns.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Analyze overall sales performance.
2. Calculate total revenue and quantity sold.
3. Identify peak and off-peak sales hours.
4. Compare revenue performance across store locations.
5. Analyze product category performance.
6. Identify high-demand product types.
7. Analyze product-level sales performance.
8. Create visualizations to communicate important findings.
9. Provide business insights based on the available data.

---

## 📊 Dataset

The dataset used in this project is:

**Afficionado Coffee Roasters.xlsx**

The dataset contains transaction-level information including:

- `transaction_id`
- `year`
- `transaction_time`
- `transaction_qty`
- `store_id`
- `store_location`
- `product_id`
- `unit_price`
- `product_category`
- `product_type`
- `product_detail`

### Dataset Limitation

The dataset contains a **transaction time** but does not contain an actual transaction date.

Therefore, genuine analysis of:

- Day of week
- Month
- Weekly trends
- Monthly trends
- Daily sales trends

cannot be reliably performed from this dataset.

The analysis therefore focuses on **time-of-day and other available dimensions**.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook
- Microsoft Excel

---

## 📁 Project Structure

```text
Afficionado-Coffee-Sales-Analysis/
│
├── data/
│   └── Afficionado Coffee Roasters.xlsx
│
├── notebooks/
│   └── sales_analysis.ipynb
│
├── README.md
│
└── requirements.txt