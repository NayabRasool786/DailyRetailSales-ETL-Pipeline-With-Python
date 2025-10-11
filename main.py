# main.py
from pyspark.sql import SparkSession
from ingest import ingest_sales_data
from enrich import enrich_with_weather
from transform_and_load import transform_and_load

def main():
    """
    Main function to run the complete ETL pipeline.
    """
    # Initialize Spark Session
    spark = SparkSession.builder.appName("DailyRetailSalesETL").getOrCreate()
    
    # Define configuration
    base_data_path = "/Workspace/Users/nayabshaik046@gmail.com/Drafts"
    final_table_name = "la_retail_sales"
    
    # 1. Ingest Data
    raw_df = ingest_sales_data(base_path=base_data_path)
    
    if raw_df.empty:
        print("No data ingested. Exiting pipeline.")
        return
        
    # 2. Enrich Data
    enriched_df = enrich_with_weather(df=raw_df, spark=spark)
    
    # 3. Transform and Load Data
    transform_and_load(df=enriched_df, spark=spark, table_name=final_table_name)
    
    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()