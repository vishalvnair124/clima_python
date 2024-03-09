import mysql.connector

# Define db_config globally
db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "database": "clima_db",
}

def get_hourly_weather(date_str, hour):
    try:
        # Establish a connection to the database
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Execute the query to fetch weather data for the specified date and hour
        query = f"SELECT * FROM weather_data WHERE DATE(Wt_recordedtime) = '{date_str}' AND HOUR(Wt_recordedtime) = {hour}"
        mycursor.execute(query)

        # Fetch the first result
        hourly_weather = mycursor.fetchone()

        if hourly_weather:
            recorded_time = hourly_weather[12]
            recorded_date = recorded_time.date()
            recorded_time_formatted = recorded_time.strftime("%I:%M:%S %p")

            result = {
                "Weather_id": hourly_weather[0],
                "Temperature": hourly_weather[1],
                "Humidity": hourly_weather[2],
                "Pressure": hourly_weather[3],
                "Rainfall": hourly_weather[4],
                "UV_Index": hourly_weather[5],
                "Wind_Speed": hourly_weather[6],
                "Wind_Direction": hourly_weather[7],
                
                "CO_Level": hourly_weather[8],
                "PM2.5": hourly_weather[9],
                "SO2_Level": hourly_weather[10],
                "NO2_Level": hourly_weather[11],
                "Recorded_Time": recorded_time_formatted,
                "Recorded_Date": recorded_date.isoformat()
            }
            return result
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor and database connection
        mycursor.close()
        mydb.close()


