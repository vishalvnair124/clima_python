import mysql.connector

def get_user_data(user_email):
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

        # Execute a query to fetch data from the 'clima_user' table
        query = f"SELECT user_name FROM clima_users WHERE user_email = '{user_email}'"
        mycursor.execute(query)

        # Fetch the user data
        user_data = mycursor.fetchone()

        if user_data:
            return {"user_email": user_email, "user_name": user_data[0]}
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor and database connection
        mycursor.close()
        mydb.close()

