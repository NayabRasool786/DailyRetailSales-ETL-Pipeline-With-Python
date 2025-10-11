# ingest.py
import pandas as pd

def ingest_sales_data(base_path: str) -> pd.DataFrame:
    """
    Reads 20 daily sales CSV files, merges them, and returns a single DataFrame.

    Args:
        base_path: The workspace path to the directory containing the sales CSVs.

    Returns:
        A pandas DataFrame containing the combined sales data.
    """
    print("Starting data ingestion...")
    
    # Create an empty DataFrame to hold all the daily sales data.
    la_sales_df = pd.DataFrame()

    # Loop through the 20 days of sales data, reading each CSV.
    for day in range(1, 21):
        # Construct the file path for each day.
        file_path = f"{base_path}/sales_2024-09-{day:02d}.csv"
        try:
            day_df = pd.read_csv(file_path)
            # Append the daily data to the main DataFrame.
            la_sales_df = pd.concat([la_sales_df, day_df], ignore_index=True)
        except FileNotFoundError:
            print(f"Warning: File not found at {file_path}. Skipping.")

    print(f"Ingestion complete. Total rows: {len(la_sales_df)}")
    return la_sales_df