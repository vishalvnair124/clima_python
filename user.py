import mysql.connector
import bcrypt
from fastapi import HTTPException
import check



# Hashing a password
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def add_user(user_name: str, user_email: str, user_password: str):
    if check.email_exists(user_email):
        raise HTTPException(status_code=409, detail="Email already exists")

    db_config = {
        "host": "localhost",
        "user": "root",
        "passwd": "",
        "database": "clima_db",
    }

    mycursor = None
    mydb = None

    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Calculate the new user_id
        mycursor.execute("SELECT COUNT(*) FROM clima_users")
        count = mycursor.fetchone()[0]
        user_id = "u" + str(count + 1)

        # Insert the new user with the calculated user_id
        query = "INSERT INTO clima_users (user_id, user_name, user_email, user_password) VALUES (%s, %s, %s, %s)"
        values = (user_id, user_name, user_email, hash_password(user_password))
        mycursor.execute(query, values)

        mydb.commit()

        return {"user_id": user_id, "user_name": user_name, "user_email": user_email, "user_password": user_password}

    except mysql.connector.Error as err:
        print(f"Error adding user: {err}")
        return None

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()
