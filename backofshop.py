import smtplib, os
from email.message import EmailMessage
from datetime import date
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.environ.get("email")
APP_PW =  os.environ.get("app_pw")
TO_ADDRESS = os.environ.get("email")
SMTP_SERVER = os.environ.get("smtp_server")
TODAY = str(date.today())


## Contact Email
def contact_email(sender_name, sender_email, sender_number, sender_message):
    connection = smtplib.SMTP(SMTP_SERVER)
    connection.starttls()
    connection.login(user=EMAIL, password=APP_PW)

    body = f"Message from: {sender_name}\nSender email: {sender_email}\nSender Phone Number: {sender_number}\n\nMessage:\n"
    body += sender_message
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = f"Customer Message from: {sender_name} on {TODAY}"
    msg["from"] = EMAIL
    msg["to"] = TO_ADDRESS

    connection.send_message(msg)
    connection.close()


# Order Confirmation Email
def order_confirmation_email(customer_name, order_number, order_details):
    connection = smtplib.SMTP(SMTP_SERVER)
    connection.starttls()
    connection.login(user=EMAIL, password=APP_PW)

    body = f"{customer_name}, your order placed on {TODAY} is in!\n\nOrder_number: {order_number}\n\n"
    body += order_details
    body += "\n\n\nThis is a demo for a project. No actual order was placed."

    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = f"Python & Bugs Order Confirmation: {order_number}"
    msg["from"] = EMAIL
    msg["to"] = TO_ADDRESS

    connection.send_message(msg)
    connection.close()