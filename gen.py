import mysql.connector
from datetime import datetime, timedelta
import random

# MySQL connection details
db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "database": "clima_db",
}

# Function to generate random weather data within realistic ranges
def generate_random_weather():
    return (
        round(random.uniform(15, 35), 2),    # Temperature (15-35°C)
        round(random.uniform(40, 80), 2),    # Humidity (40-80%)
        round(random.uniform(980, 1020), 2),# Pressure (980-1020 hPa)
        round(random.uniform(0, 10), 2),    # Rainfall (0-10 mm)
        round(random.uniform(0, 10), 2),    # UV Index (0-10)
        round(random.uniform(0, 20), 2),    # Wind Speed (0-20 m/s)
        random.randint(0, 80),             # Wind Direction (0-360 degrees)
        round(random.uniform(0, 300), 2),   # Air Quality Index (0-300)
        round(random.uniform(0, 5), 2),     # CO Level (0-5 ppm)
        round(random.uniform(0, 50), 2),    # PM2.5 (0-50 µg/m³)
        round(random.uniform(0, 5), 2),     # SO2 Level (0-5 ppm)
        round(random.uniform(0, 5), 2)      # NO2 Level (0-5 ppm)
    )

# Function to insert sample weather data
def insert_sample_weather_data(num_days=10):
    try:
        # Establish a connection to the database
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Start date for generating data (10 days ago from today)
        start_date = datetime.now() - timedelta(days=num_days)

        # Generate and insert weather data for each hour of each day
        for i in range(num_days):
            for j in range(24):
                weather_datetime = start_date + timedelta(days=i, hours=j)
                weather_data = generate_random_weather()
                query = "INSERT INTO weather_data (Wt_temp, Wt_hum, Wt_pre, Wt_rain, Wt_uv, Wt_windspeed, Wt_winddir, Wt_aqi, Wt_co, Wt_pmtwo, Wt_sotwo, Wt_notwo, Wt_recordedtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor.execute(query, weather_data + (weather_datetime,))
        
        # Commit the transaction
        mydb.commit()
        print("Sample weather data inserted successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and database connection
        mycursor.close()
        mydb.close()

# Call the function to insert sample weather data for 10 days
insert_sample_weather_data(10)
