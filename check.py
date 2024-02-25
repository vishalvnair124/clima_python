import mysql.connector

def email_exists(email):
    db_config = {
        "host": "localhost",
        "user": "root",
        "passwd": "",
        "database": "clima_db",
    }

    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        query = "SELECT COUNT(*) FROM clima_users WHERE user_email = %s"
        mycursor.execute(query, (email,))
        count = mycursor.fetchone()[0]

        return count > 0

    except mysql.connector.Error as err:
        print(f"Error checking email existence: {err}")
        return False

    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()
