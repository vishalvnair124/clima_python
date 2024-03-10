# auth_utils.py

import mysql.connector
from pydantic import BaseModel
import bcrypt

# Model for update password request body
class UpdatePasswordRequest(BaseModel):
    user_email: str
    current_password: str
    new_password: str

# Function to authenticate user
def authenticate_user(email: str, password: str) -> bool:
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
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error authenticating user: {err}")
        return False
    finally:
        mycursor.close()
        mydb.close()

# Function to update user password
def update_password(user_email: str, new_password: str) -> bool:
    db_config = {
        "host": "localhost",
        "user": "root",
        "passwd": "",
        "database": "clima_db",
    }
    
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        query = "UPDATE clima_users SET user_password = %s WHERE user_email = %s"
        mycursor.execute(query, (hashed_password.decode('utf-8'), user_email))
        mydb.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating password: {err}")
        return False
    finally:
        mycursor.close()
        mydb.close()
