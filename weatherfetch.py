# weatherfetch.py
import mysql.connector
import datetime
def get_latest_weather():
    # Replace these with your actual MySQL connection details
    db_config = {
        "host": "localhost",
        "user": "root",
        "passwd": "",
        "database": "clima_db",
    }

    try:
        # Establish a connection to the database
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Execute the query to fetch the row with the maximum Weather_id
        query = "SELECT * FROM weather_data WHERE Weather_id = (SELECT MAX(Weather_id) FROM weather_data)"
        mycursor.execute(query)

        # Fetch the result
        latest_weather = mycursor.fetchone()

        if latest_weather:
            # Convert the result to a dictionary for JSON serialization
            recorded_time = latest_weather[13]
            recorded_date = recorded_time.date() 
            recorded_time_formatted = recorded_time.strftime("%I:%M:%S %p")
            result = {
               "Weather_id": latest_weather[0],
               "Temperature": latest_weather[1],
               "Humidity": latest_weather[2],
               "Pressure": latest_weather[3],
               "Rainfall": latest_weather[4],
               "UV_Index": latest_weather[5],
               "Wind_Speed": latest_weather[6],
               "Wind_Direction": latest_weather[7],
               "Air_Quality_Index": latest_weather[8],
               "CO_Level": latest_weather[9],
               "PM2.5": latest_weather[10],
               "SO2_Level": latest_weather[11],
               "NO2_Level": latest_weather[12],
               "Recorded_Time": recorded_time_formatted ,
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
