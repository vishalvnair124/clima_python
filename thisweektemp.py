import mysql.connector

# Define db_config globally
db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "database": "clima_db",
}

# Connect to the database
try:
    connection = mysql.connector.connect(**db_config)
    print("Connected to MySQL database!")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Fetch daily average data from the last 7 days
    query = """
    SELECT DATE(Wt_recordedtime) AS Date,
           AVG(Wt_temp) AS Avg_Temperature,
           AVG(Wt_hum) AS Avg_Humidity,
           AVG(Wt_pre) AS Avg_Pressure,
           AVG(Wt_co) AS Avg_CO,
           AVG(Wt_sotwo) AS Avg_SO2,
           AVG(Wt_notwo) AS Avg_NO2,
           AVG(Wt_pmtwo) AS Avg_PM_2_5
    FROM weather_data
    WHERE Wt_recordedtime >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
    GROUP BY DATE(Wt_recordedtime)
    """
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Construct the formatted string
    formatted_data = "Date,Temperature,Humidity,Pressure,CO,SO2,NO2,PM 2.5\n"
    for row in rows:
        formatted_data += f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]}\n"

    # Print the formatted data
    print(formatted_data)

    # Close cursor and connection
    cursor.close()
    connection.close()

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL database: {e}")



import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from io import StringIO
import pickle

# Load the fitted models from pickle file
with open('arima_models.pkl', 'rb') as f:
    loaded_models = pickle.load(f)

# Sample 7-day data
sample_data = formatted_data

# Convert sample data string to DataFrame
sample_df = pd.read_csv(StringIO(sample_data), parse_dates=['Date'], index_col='Date')

# Forecast future values for each variable using the loaded ARIMA models
forecasts = {}
for variable, model in loaded_models.items():
    forecasts[variable] = model.forecast(steps=6)

print("Forecasts:")
for variable, forecast_values in forecasts.items():
    print(f"{variable}: {forecast_values}")

def get_forecast_weather():
    result = {
        "Temperature": forecasts['Temperature'],
    }
    return result

# Call the function to get forecasted values
forecasted_values = get_forecast_weather()
print("\nForecasted Values:")
print(forecasted_values)
