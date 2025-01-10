import os
import time
import json
import yagmail
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

### USER MUST CREATE CREDETNIAS.JSON FILE WITH SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL ### THERE MUST BE AN EASIER WAY TO DO THIS ###
with open("credentials.json", "r") as f:
    credentials = json.load(f)
    SENDER_EMAIL = credentials["SENDER_EMAIL"]
    SENDER_PASSWORD = credentials["SENDER_PASSWORD"]
    RECEIVER_EMAIL = credentials["RECEIVER_EMAIL"]


def send_email_notification(event_type, details=""):
    try:
        email = yagmail.SMTP(user=SENDER_EMAIL, password=SENDER_PASSWORD)
        subject = f"WoW {event_type} event occured"
        body = f"Event: {event_type}\nDetails: {details}"
        email.send(to=RECEIVER_EMAIL, subject=subject, contents=body)
    except Exception as e:
        print(f"Error sending email: {e}")

# TO DO


class WoWLogHandler(FileSystemEventHandler):
    pass


def main():
    user_input = input("send mail? (y/n): ")
    if user_input == "y":
        send_email_notification("test", "this is a test email")
    else:
        print("Exiting...")


if __name__ == "__main__":
    main()
