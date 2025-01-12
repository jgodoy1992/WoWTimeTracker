import os
import time
from datetime import datetime
import json
import yagmail
import pandas as pd
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
    WOW_TIME_EXCEL = file_paths["WOW_TIME_EXCEL"]

### EMAIL FUCNTION ###


def send_email_notification(event_type, details="") -> None:
    try:
        email = yagmail.SMTP(user=SENDER_EMAIL, password=SENDER_PASSWORD)
        subject = f"WoW {event_type} event occured"
        body = f"Event: {event_type}\nDetails: {details}"
        email.send(to=RECEIVER_EMAIL, subject=subject, contents=body)
    except Exception as e:
        print(f"Error sending email: {e}")

# TO DO: CSV or XLSX file creator class

### GENERATE EXCEL FILE ###


class WoWToExcel:
    def __init__(self, logout_time: datetime, played_time: datetime):
        self.logout_time = logout_time
        self.played_time = played_time

    # Convert played_time object to minutes
    def _to_minutes(self) -> float:
        return round(self.played_time.seconds/60, 2)

    # Function to load to Excel file. If the file exists then it updates it. If not then creates on and inputs data
    def load_to_excel(self) -> None:

        minutes = self._to_minutes()
        df = pd.DataFrame(
            {
                "Date": [self.logout_time.strftime('%y-%m-%d')],
                "Time played": [minutes]
            }
        )

        if os.path.exists(WOW_TIME_EXCEL):
            with pd.ExcelWriter(WOW_TIME_EXCEL, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name="Time spent",
                            startrow=writer.sheets["Time spent"].max_row, index=False, header=False)
        else:
            with pd.ExcelWriter(WOW_TIME_EXCEL, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Time spent", index=False)

### HANDLER CLASS ###


class WoWLogHandler(FileSystemEventHandler):
    def __init__(self, log_file_path):
        self.log_file_path = os.path.abspath(log_file_path)
        self.login_email_sent = False
        self.logout_email_sent = False
        self.login_time = None

        # When the object is created it looks for the log file and check if it exist and is empty. If it is, then it sends the email to the user
        if os.path.exists(self.log_file_path) and os.path.getsize(self.log_file_path) == 0:
            print("login has occured")
            self.login_time = datetime.now()
            details = self.login_time.strftime('%y-%m-%d %H:%M:%S')
            send_email_notification("login", details)
            self.login_email_sent = True

    # Uses watchdog's on_modified method to check if the log file is modified. If it is and satisfies the stablished criteria, the it sends email to the user.
    def on_modified(self, event):
        event_path = os.path.abspath(event.src_path)
        if event_path == self.log_file_path:
            print("source found")
            with open(self.log_file_path, "r") as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    if "WowConnectionNet: Shutdown" in last_line and not self.logout_email_sent:
                        if self.login_time:
                            logout_time = datetime.now()
                            play_duration = logout_time - self.login_time
                            formated_duration = str(
                                play_duration).split(".")[0]
                            details = f"Details : {
                                last_line}\n Playtime {formated_duration}"
                            to_excel = WoWToExcel(
                                logout_time, play_duration)
                            to_excel.load_to_excel()
                        else:
                            details = f"Details : {
                                last_line}\n Playtime Unkown"
                        print("logout occured")
                        send_email_notification("logout", details)
                        self.logout_email_sent = True


def main():

    if not LOG_FILE_PATH:
        print(f"Log file {LOG_FILE_PATH} not found")
        exit(1)

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
