# 🛒 Daily Retail Sales ETL Pipeline

This project contains a robust, modular, and automated **ETL (Extract, Transform, Load)** pipeline designed to process daily retail sales data.  
The pipeline is built with **Python** and is optimized to run as a scheduled job on the **Databricks** platform.

The core function of this pipeline is to ingest raw daily sales files, enrich them with external data (in this case, weather information), perform necessary cleaning and transformations, and load the final, analysis-ready data into a **Delta table**.

---

## 🏛️ Project Architecture

The pipeline follows a standard **multi-stage ETL process**. Data flows from raw source files to a final, clean table, with each stage being handled by a dedicated module.  
This modular design makes the pipeline easy to maintain, debug, and scale.

The flow of data can be visualized as follows:

![ETL Workflow Diagram](/Images/ETL-Workflow-Diagram.png)

- **Extract:** Raw daily sales data is ingested from multiple CSV files.  
- **Transform & Enrich:** The combined data is enriched by calling an external weather API. It is cleaned, transformed, and new metrics are calculated.  
- **Load:** The final, processed data is loaded into a structured Delta Lake table, ready for analytics, BI reporting, or machine learning.

---

## ✨ Key Features

- **Modular Code:** The logic is split into distinct Python files for ingestion, enrichment, and transformation, promoting code reusability and clarity.  
- **Automation-Ready:** Designed to be executed as an automated, scheduled Databricks Job for daily processing.  
- **Data Enrichment:** Calls the OpenWeatherMap API to fetch historical weather data, adding valuable context to the sales information.  
- **Secure Credential Management:** Uses Databricks Secrets to securely store and access the API key, avoiding hardcoded credentials.  
- **Scalability:** Built on Spark (via Databricks), the pipeline can scale to handle large volumes of data.  
- **Reliability:** Uses Delta Lake tables as the final destination, ensuring data reliability and transactional integrity.

---

## 📂 Code Structure

The project is organized into modular Python scripts, each with a specific responsibility.  
The `main.py` script acts as the orchestrator that calls the functions from the other modules in sequence.

| File | Description |
|------|--------------|
| **main.py** | The entry point of the application. It orchestrates the entire ETL flow by calling functions from the other modules in the correct order. |
| **ingest.py** | Handles the "Extract" phase. Contains the logic to find and read the 20 daily sales CSV files and combine them into a single DataFrame. |
| **enrich.py** | Handles the "Enrichment" part of the "Transform" phase. It takes the raw data, calls the weather API, and merges the temperature data. |
| **transform_and_load.py** | Handles the final "Transform" and "Load" phases. It cleans the data, calculates new columns (like `rev_per_unit`), and saves the result. |

---

## 🚀 How to Run the Pipeline on Databricks

Follow these steps to deploy and run this ETL pipeline in your Databricks workspace.

---

### ✅ Prerequisites

- A Databricks workspace.  
- Your daily sales CSV files uploaded to a known location in the Databricks File System (DBFS) or Workspace.  
- An API key from **OpenWeatherMap**.  
- Databricks Secrets Setup: You must create a secret scope and add your API key to it.

#### Steps to set up secrets:
1. Create a scope (e.g., `nayabrasool786`).  
2. Add your key with a name (e.g., `openweathermap-api-key`).

---

### 🧩 Step 1: Upload the Python Files

Upload all four Python files (`main.py`, `ingest.py`, `enrich.py`, `transform_and_load.py`) to your Databricks Workspace.

![Upload Python Files to Workspace](/Images/Upload-Python-Files-to-Workspace.png)

---

### ⚙️ Step 2: Create a Databricks Job

1. Navigate to the **Workflows** section in Databricks and click **Create Job**.  
2. Create a new task and configure it as follows:

- **Task name:** A descriptive name like `Daily_Retail_ETL`.  
- **Type:** Select `Python script`.  
- **Source:** Workspace.  
- **Path:** Use the browser to select the `main.py` file you uploaded.  
- **Compute:** Use **Serverless** for automatic compute management or configure a specific Job Cluster.  
- **Dependent Libraries:** Click **+ Add** and add the following packages from PyPI:
  - `pandas`
  - `requests`
  - `databricks-sql-connector`

![Databricks Job Task Configuration](/Images/Databricks-Job-Task-Configuration.png)

---

### ▶️ Step 3: Run the Job

Click the **Run now** button to execute the pipeline.  
You can monitor the run's progress in the **Job runs** tab.

![Successful Job Run Monitoring](/Images/Successful-Job-Run-Monitoring.png)

---

## 🔧 Configuration

The main settings for the pipeline can be easily modified in the `main.py` file:

```python
# main.py

def main():
    # ...
    
    # --- Configuration ---
    # Update this path to point to the location of your CSV files.
    base_data_path = "/Workspace/Users/your_email@domain.com/path/to/data"
    
    # Change this to the desired name for your final Delta table.
    final_table_name = "la_retail_sales_final"
    
    # ...
