#Directly connect to Gmail mail server, where Gmail will be the "transport", send the email after writing logic

#for email sending 
import smtplib

#for email formating 
from email.mime.text import MIMEText

from config import SMTP_SERVER, SMTP_PORT, USERNAME, PASSWORD, RECEIVER

# SMTP_SERVER = "smtp.office365.com" # OR smtp.gmail.com
# SMTP_PORT = 587  # OR 465?
# USERNAME = "logan.laszewski@gmail.com"
# PASSWORD = "16 character app password"
# RECEIVER = "logan.laszewski@comcast.net"


BODY = "This is a test email from smtplib package in Python"
MESSAGE = MIMEText(BODY, "plain")
MESSAGE["Subject"] = "SMTP test"
MESSAGE["From"] = USERNAME
MESSAGE["To"] = RECEIVER


with smtplib.SMTP(SMTP_SERVER,SMTP_PORT, timeout = 10) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(USERNAME,PASSWORD)
    server.sendmail(USERNAME,[RECEIVER],MESSAGE.as_string())