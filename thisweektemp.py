import mysql.connector
import pandas as pd
import pickle
from pmdarima import auto_arima
from datetime import datetime, timedelta

# Define db_config globally
db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "database": "clima_db",
}

def get_today_temp(cursor):
    today = datetime.now().date()
    query = f"""
    SELECT AVG(Wt_temp) AS Avg_Temperature
    FROM weather_data
    WHERE DATE(Wt_recordedtime) = '{today}'
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row else None

# Connect to the database
try:
    connection = mysql.connector.connect(**db_config)
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
    rows = cursor.fetchall()

    # Convert fetched data into a DataFrame
    columns = ['Date', 'Temperature', 'Humidity', 'Pressure', 'CO', 'SO2', 'NO2', 'PM 2.5']
    data = pd.DataFrame(rows, columns=columns)

    # Load the fitted models from pickle file
    with open('arima_models.pkl', 'rb') as f:
        loaded_models = pickle.load(f)

    # Retrain ARIMA models on the combined data
    retrained_models = {}
    for variable in loaded_models:
        model = auto_arima(data[variable], seasonal=False, suppress_warnings=True)
        retrained_models[variable] = model

    # Forecast future values for each variable using the retrained ARIMA models
    forecasts = {}
    for variable, model in retrained_models.items():
        forecasts[variable] = model.predict(n_periods=6)

    # Get today's temperature
    today_temp = get_today_temp(cursor)

    def get_thisweektemp_weather():
        result = {
            "Today_Temperature": today_temp,
            "Temperature": forecasts['Temperature'],
          
        }
        return result

    # Call the function to get forecasted values
    forecasted_values = get_thisweektemp_weather()
    # print("\nForecasted Values:")
    # print(forecasted_values)

    # Close cursor and connection
    cursor.close()
    connection.close()

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL database: {e}")
