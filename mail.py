# mail.py

from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailData(BaseModel):
    user_email: str
    otp: str

def send_email(user_email, otp):
    # Configure email server
    sender_email = "database71231@gmail.com"  # Replace with your email
    sender_password = "emss jdao gbko canb"  # Replace with your email password
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server address
    smtp_port = 587  # Replace with your SMTP server port

    # Generate email content
    message = MIMEMultipart()
    message['From'] = "database71231@gmail.com"
    message['To'] = user_email
    message['Subject'] = "Your One Time Password (OTP)"

    body = f"Your OTP is: {otp}"

    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
