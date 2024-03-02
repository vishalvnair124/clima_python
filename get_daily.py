import mysql.connector

# Define db_config globally
db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "database": "clima_db",
}

def get_daily_weather(date_str):
    try:
        # Establish a connection to the database
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Execute the query to fetch weather data for the specified date
        query = f"SELECT * FROM weather_data WHERE DATE(Wt_recordedtime) = '{date_str}'"
        mycursor.execute(query)

        # Fetch the result
        hourly_weather = mycursor.fetchall()

        # Check if any data is returned
        if not hourly_weather:
            return None

        result = {}
        for i, record in enumerate(hourly_weather):
            recorded_time = record[13]
            recorded_date = recorded_time.date()
            recorded_time_formatted = recorded_time.strftime("%I:%M:%S %p")

            weather_data = {
                "Weather_id": record[0],
                "Temperature": record[1],
                "Humidity": record[2],
                "Pressure": record[3],
                "Rainfall": record[4],
                "UV_Index": record[5],
                "Wind_Speed": record[6],
                "Wind_Direction": record[7],
                "Air_Quality_Index": record[8],
                "CO_Level": record[9],
                "PM2.5": record[10],
                "SO2_Level": record[11],
                "NO2_Level": record[12],
                "Recorded_Time": recorded_time_formatted,
                "Recorded_Date": recorded_date.isoformat()
            }
            result[str(i)] = weather_data

        return result

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor and database connection
        mycursor.close()
        mydb.close()

