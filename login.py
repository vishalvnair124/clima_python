import mysql.connector
from fastapi import HTTPException
import bcrypt

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(email, password):
    db_config = {
        "host": "localhost",
        "user": "root",
        "passwd": "",
        "database": "clima_db",
    }

    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        query = "SELECT user_password FROM clima_users WHERE user_email = %s"
        mycursor.execute(query, (email,))
        result = mycursor.fetchone()

        if result:
            hashed_password = result[0]
            if verify_password(password, hashed_password):
                return True
            else:
                return False
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Error authenticating user: {err}")
        return False

    finally:
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()
