# CSV Data Cleaner

A simple Streamlit web application for uploading, exploring, and cleaning CSV datasets.  
It provides basic data profiling and automated cleaning features with an option to download the cleaned file.

---

## 🚀 Features

### 📊 Dataset Overview
- Displays number of rows and columns
- Shows total missing values
- Shows number of duplicate rows
- Identifies column with most missing values
- Preview of full dataset

### 🧹 Data Cleaning
The app performs the following cleaning steps:

- Removes duplicate rows
- Converts common missing values (`N/A`, `NA`, `null`, etc.) into standard NaN
- Drops columns with more than 50% missing values
- Detects and processes column types:
  - **Numeric columns** → missing values filled with median
  - **Datetime columns** → missing values filled using forward/backward fill
  - **Text columns** → cleaned and missing values replaced with `"Unknown"`
- Standardizes column names (lowercase, underscores)

---

## 📈 Before vs After Comparison
After cleaning, the app shows:
- Row count comparison
- Missing values before and after cleaning
- Duplicate rows before and after cleaning

---

## 💾 Download
Users can download the cleaned dataset as a CSV file.

---

## 🛠️ Tech Stack
- Python
- Streamlit
- Pandas
- NumPy

---
