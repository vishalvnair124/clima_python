# random_password.py

import random
import string
from auth_utils import update_password, authenticate_user
from mail import send_email

def generate_random_password():
    # Define sets of characters for generating password
    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?/~"
    digits = string.digits
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase

    # Randomly choose characters from each set
    password = ''.join(random.choice(special_characters) +
                       random.choice(digits) +
                       random.choice(lowercase_letters) +
                       random.choice(uppercase_letters) +
                       random.choice(string.ascii_letters + string.digits) 
                       for _ in range(2))

    # Shuffle the password to ensure random distribution of characters
    password = ''.join(random.sample(password, len(password)))

    # Add random characters to meet the 6-character requirement
    while len(password) < 6:
        password += random.choice(string.ascii_letters + string.digits)

    return password

def update_and_notify_password(user_email):
    # Generate a random password
    new_password = generate_random_password()

    # Update password in the database
    if update_password(user_email, new_password):
        # Send the new password via email
        if send_new_password_email(user_email, new_password):
            return True
        else:
            return False
    else:
        return False

def send_new_password_email(user_email, new_password):
    
    message = f"Your new password is: {new_password}"
    return send_email(user_email, message)
