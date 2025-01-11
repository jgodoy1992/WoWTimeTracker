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

### USER MUST CREATE FILE_PATHS.JSON FILE WITH LOG_FILE_PATH ###

with open("file_paths.json", "r") as f:
    file_paths = json.load(f)
    LOG_FILE_PATH = file_paths["LOG_FILE_PATH"]


def send_email_notification(event_type, details=""):
    try:
        email = yagmail.SMTP(user=SENDER_EMAIL, password=SENDER_PASSWORD)
        subject = f"WoW {event_type} event occured"
        body = f"Event: {event_type}\nDetails: {details}"
        email.send(to=RECEIVER_EMAIL, subject=subject, contents=body)
    except Exception as e:
        print(f"Error sending email: {e}")

# TO DO: WoWLogHandler class + CSV or XLSX file creator class


class WoWLogHandler(FileSystemEventHandler):
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.login_email_sent = False
        self.logout_email_sent = False
        self.login_time = None

        if os.path.getsize(self.log_file_path) == 0:
            print("login has occured")
            send_email_notification("login")
            self.login_email_sent = True


def main():
    event_handler = WoWLogHandler(LOG_FILE_PATH)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(
        LOG_FILE_PATH), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
