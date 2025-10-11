# enrich.py
import pandas as pd
import requests
import time
from datetime import datetime

# In a Databricks environment, dbutils is available automatically.
# When running locally, you would need to mock this.
from pyspark.sql import SparkSession

def get_dbutils(spark: SparkSession):
    """
    Returns the dbutils object if in a Databricks environment.
    """
    try:
        from pyspark.dbutils import DBUtils
        dbutils = DBUtils(spark)
    except ImportError:
        import IPython
        dbutils = IPython.get_ipython().user_ns["dbutils"]
    return dbutils


def enrich_with_weather(df: pd.DataFrame, spark: SparkSession) -> pd.DataFrame:
    """
    Enriches the sales DataFrame with temperature data from the OpenWeatherMap API.

    Args:
        df: The input pandas DataFrame with a 'date' column.
        spark: The active SparkSession to access dbutils.

    Returns:
        A pandas DataFrame with an added 'temp' column.
    """
    print("Starting data enrichment...")
    
    dbutils = get_dbutils(spark)
    
    # Securely get the API key from Databricks secrets.
    API_KEY = dbutils.secrets.get(scope="nayabrasool786", key="openweathermap-api-key")
    LAT, LON = 34.0522, -118.2437
    
    weather_data = []

    # Get a list of unique dates to avoid redundant API calls.
    dates = df['date'].sort_values().dropna().unique()

    for date in dates:
        unix_timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp())
        url = (
            f"https://api.openweathermap.org/data/3.0/onecall/timemachine"
            f"?lat={LAT}&lon={LON}&dt={unix_timestamp}&appid={API_KEY}&units=imperial"
        )
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching weather for {date}: {response.status_code}")
        else:
            data = response.json()
            day_weather = {
                "date": date,
                "temp": data["data"][0]["temp"],
            }
            weather_data.append(day_weather)
        
        time.sleep(1) # Be respectful of the API rate limits.

    # Create a DataFrame from the fetched weather data.
    weather_df = pd.DataFrame(weather_data)
    print(f"Successfully fetched weather data for {len(weather_df)} dates.")

    # Merge the weather data back into the main sales DataFrame.
    enriched_df = df.merge(weather_df, how="left", on="date")
    
    print("Enrichment complete.")
    return enriched_df