# 🌍 Country Data Cleaning Project

## 🧾 Overview
This project focuses on **cleaning** and **standardizing** a raw dataset containing information about world countries, including economic, demographic, and statistical indicators.  
The cleaning process ensures the data is consistent, usable, and ready for analysis or machine learning.

---

## 📂 Files Included
- `Country.csv` – Original raw dataset.
- `Country_CLEANED.csv` – Cleaned and transformed dataset.
- `Clean.py` – Python script that cleans and processes the data (with inline comments).
- `README.md` – Documentation of the project purpose, logic, and methodology.

---

## 🛠️ Data Cleaning Steps

### 1. Removing Aggregates:
Filtered out non-country/aggregate entries such as:
- "Arab World"
- "Euro Area"
- "OECD"
- "World", etc.

### 2. Renaming and Dropping Columns:
- `ShortName` ➜ `CountryName`
- `LongName` ➜ `CountryLongName`
- Dropped: `TableName`, `Wb2Code`, `SystemOfNationalAccounts`, `LatestHouseholdSurvey`, `SourceOfMostRecentIncomeAndExpenditureData`, etc.

### 3. Standardizing Codes:
- Fixed `Alpha2Code` for special cases like:
  - Kosovo ➜ `XK`
  - Namibia ➜ `NA`

### 4. Extracting & Cleaning Year Fields:
- Extracted 4-digit years using regex from fields like:
  - `LatestPopulationCensus`
  - `PppSurveyYear`
  - `NationalAccountsBaseYear`
  - `BalanceOfPaymentsManualInUse`
- Filled missing values with `0` or `"Unknown"` where appropriate.

### 5. Standardizing Text Columns:
- Unified `IncomeGroup` values (e.g., `"Upper income"` ➜ `"Upper middle income"`)
- Extracted codes from parentheses in fields like `SnaPriceValuation`, `ImfDataDisseminationStandard`, `SourceOfMostRecentIncome`

---

## 📌 Notes
- Project uses **Pandas** in Python for all data wrangling.
- Designed for reproducibility and future extension (e.g., visualizations, ML models).

---

## 📊 Example Use Case
This cleaned dataset can be used in:
- Comparative economic analysis.
- Data visualization dashboards.
- Machine learning projects on global development.

🧠 Author
Name: ASSIEL OSAMA
University: Imam Mohammad Ibn Saud Islamic University
Major: Information Systems
Certification: Google Data Analytics, IBM (BI) Analytics
LinkedIn: www.linkedin.com/in/assiel-alsrdide-a2aa95264





