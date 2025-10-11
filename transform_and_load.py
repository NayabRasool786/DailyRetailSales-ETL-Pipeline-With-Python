# transform_and_load.py
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession

def transform_and_load(df: pd.DataFrame, spark: SparkSession, table_name: str):
    """
    Performs final transformations and saves the DataFrame to a Delta table.

    Args:
        df: The enriched pandas DataFrame.
        spark: The active SparkSession.
        table_name: The name of the final Delta table to write to.
    """
    print("Starting final transformation and load...")

    # --- Transformation Step ---
    df["date"] = pd.to_datetime(df["date"])
    df["unit_sales"] = df["unit_sales"].fillna(0)
    df.dropna(subset=["dollar_sales"], inplace=True)

    # Calculate revenue per unit, handling division by zero.
    df["rev_per_unit"] = (df["dollar_sales"] / df["unit_sales"]).round(2)
    df.replace([np.inf, -np.inf], 0, inplace=True)

    # Clean string data and correct data types.
    df["store_zip"] = df["store_zip"].str.replace('XX', '00')
    df["unit_sales"] = df["unit_sales"].astype(int)
    
    print("Transformations complete.")

    # --- Load Step ---
    # Convert the final pandas DataFrame to a Spark DataFrame for saving.
    final_spark_df = spark.createDataFrame(df)

    # Save the final data to the main presentation table.
    (
        final_spark_df
        .write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )
    
    print(f"Successfully loaded final data to the '{table_name}' table.")