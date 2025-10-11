# End-to-End Data Engineering Workflow in Databricks

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python) ![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.x-orange?logo=apache-spark) ![Databricks](https://img.shields.io/badge/Databricks-CE-red?logo=databricks) ![Delta Lake](https://img.shields.io/badge/Delta%20Lake-2.x-green?logo=linux-foundation)

This repository demonstrates a complete, end-to-end data engineering workflow performed within a single Databricks notebook. The project follows a standard **IMETL (Ingest, Merge, Enrich, Transform, Load)** process, transforming raw CSV data into a clean, analysis-ready Delta table.

This project is perfect for students, aspiring data engineers, or anyone looking for a practical, hands-on example of using PySpark and Databricks for data processing.

---

##  Workflow Overview

The core of this project is to process raw sales and customer data to create a final, enriched dataset. The entire process is orchestrated within a Databricks notebook, leveraging the power of Apache Spark for distributed data processing.

The data flows through the following stages:


*(A simple diagram showing: Raw CSV Files -> Databricks DBFS -> Spark DataFrame -> Join/Enrich -> Transform -> Final Delta Table)*

---

## 🛠️ Tech Stack

* **Cloud Platform:** Databricks Community Edition
* **Core Engine:** Apache Spark (using PySpark API)
* **Language:** Python
* **Storage Format:** Delta Lake
* **Data Source:** CSV files

---

## 🚀 Getting Started

Follow these steps to replicate the project in your own Databricks environment.

### Prerequisites

* An active [Databricks Community Edition](https://community.cloud.databricks.com/) account.
* A running Databricks cluster. (A standard, single-node cluster available in the Community Edition is sufficient).

### Setup Instructions

**1. Prepare the Sample Data**

You need two CSV files. Create `sales.csv` and `customers.csv` on your local machine with the content below.

* `sales.csv`:
    ```csv
    sale_id,customer_id,product,amount
    1,101,Laptop,1200
    2,102,Mouse,25
    3,101,Keyboard,75
    4,103,Monitor,300
    5,102,Webcam,50
    ```
* `customers.csv`:
    ```csv
    customer_id,name,location
    101,Alice,USA
    102,Bob,Canada
    103,Charlie,USA
    ```

**2. Upload Data to Databricks File System (DBFS)**

* In the Databricks UI, navigate to **Catalog** > **DBFS**.
* Go into the `FileStore` directory.
* Click the **Upload** button and upload both `sales.csv` and `customers.csv`.



**3. Import the Notebook**

* Download the `.ipynb` or `.py` file from this repository.
* In your Databricks workspace, go to your user folder, click the dropdown, and select **Import**.
* Import the notebook file and attach it to your running cluster.

---

## 🔬 The Workflow Explained Step-by-Step

The notebook is divided into logical cells that correspond to each stage of the data pipeline.

### 1. Ingest: Reading Raw Data

**What it does:** This is the first step where we load our raw data from the CSV files stored in DBFS into Spark DataFrames. A DataFrame is a distributed collection of data organized into named columns, similar to a table in a database.

**The Code:**
```python
sales_path = "/FileStore/sales.csv"
customers_path = "/FileStore/customers.csv"

sales_df = spark.read.csv(sales_path, header=True, inferSchema=True)
customers_df = spark.read.csv(customers_path, header=True, inferSchema=True)

display(sales_df)
```

* `header=True` tells Spark that the first row of each CSV is the column names.
* `inferSchema=True` makes Spark automatically guess the data type for each column (e.g., `amount` becomes an integer).

**Result:** Two separate DataFrames (`sales_df` and `customers_df`) are created in Spark's memory.

[Image showing the raw sales_df DataFrame output in Databricks]

### 2. Merge & Enrich: Combining Data

**What it does:** Our sales data only has a `customer_id`. To make it more useful, we merge it with the customer data to add the customer's `name` and `location` to each sale. This process of adding more context to data is called **enrichment**. We use a **join** operation, which is a fundamental concept in data processing.

**The Code:**
```python
enriched_df = sales_df.join(customers_df, on="customer_id", how="left")

display(enriched_df)
```

* `on="customer_id"` tells Spark to match rows from both tables where the `customer_id` is the same.
* `how="left"` ensures that we keep all sales records, even if a matching customer is not found (it would show `null` values in that case).

**Result:** A single, wider DataFrame (`enriched_df`) that contains both sales and customer information in each row.

[Image showing the enriched_df DataFrame with joined columns]

### 3. Transform: Cleaning and Feature Engineering

**What it does:** This is the most critical stage where we apply business rules, clean the data, and create new, valuable information (feature engineering).

**The Code:**
```python
from pyspark.sql.functions import col, lit, upper, round

transformed_df = enriched_df.withColumn("tax", round(col("amount") * 0.08, 2)) \
                            .withColumn("source_system", lit("SalesSystem_v1")) \
                            .withColumn("location_code", upper(col("location"))) \
                            .drop("customer_id")

display(transformed_df)
```

* `withColumn("tax", ...)`: We create a new column called `tax` by calculating 8% of the `amount`.
* `withColumn("source_system", ...)`: We add a static column to track where this data came from, which is good for data lineage. `lit()` stands for "literal" and creates a constant value.
* `withColumn("location_code", ...)`: We create a new column `location_code` by converting the existing `location` column to uppercase for standardization.
* `drop("customer_id")`: We remove the `customer_id` column as it's no longer needed after the join.

**Result:** A clean, standardized, and feature-rich DataFrame (`transformed_df`) ready for loading.

[Image showing the final transformed_df with new columns like 'tax']

### 4. Load: Saving the Final Table

**What it does:** The final step is to save our processed data. We load it into a **Delta Table**. Delta Lake is a storage layer that brings reliability (ACID transactions) to data lakes, making our data robust and queryable, much like a traditional database.

**The Code:**
```python
final_table_name = "sales_transformed"

transformed_df.write.format("delta").mode("overwrite").saveAsTable(final_table_name)
```

* `format("delta")` specifies that we want to save the data in the high-performance Delta format.
* `mode("overwrite")` tells Spark to replace the table if it already exists. This makes our notebook re-runnable without errors.
* `saveAsTable(...)` saves the output as a permanent, queryable table in the Databricks metastore.

**Result:** A reliable, high-performance Delta table named `sales_transformed` is created, which can now be easily accessed for analytics, reporting, or machine learning.

---

### Verifying the Result

You can instantly query the final table using SQL in a new notebook cell to verify that the entire process was successful.

```sql
%sql
SELECT * FROM sales_transformed WHERE location_code = 'USA';
```

[Image showing the SQL query result from the final Delta table]
