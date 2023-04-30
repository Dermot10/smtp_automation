from asyncio import subprocess
from email import message
import smtplib
import os
import random
from datetime import date, time as datetime_time
from datetime import datetime, timedelta
import time
import setproctitle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from quotes_scraped import find_quote

load_dotenv()


class SMTPAutomator:
    def __init__(self):
        self.smtp_server = 'smtp.office365.com'
        self.smtp_port = 587
        self.sender_email = os.environ.get("email_user")
        self.sender_password = os.environ.get("email_password")
        self.recipient_email = os.environ.get("gmail_user")
        self.message_time = datetime_time(8, 30)

    def build_msg(self):
        """Function to build message object and the corresponding email headers"""

        msg = MIMEMultipart()
        msg['FROM'] = self.sender_email
        msg['TO'] = self.recipient_email
        msg['SUBJECT'] = 'Quote To Self'

        return msg

    def get_random_quote(self):
        """Function to get random quote for msg body"""
        return random.choice(find_quote())

    def run(self):
        """Function to build and send message. Process runs once per day"""
        msg = self.build_msg()
        body = self.get_random_quote()
        msg.attach(MIMEText(body, 'plain'))

        while True:
            now = datetime.now()

            # Create a datetime object with the same date as the current date and the desired time
            message_datetime = datetime.combine(now.date(), self.message_time)

            # If the message_datetime is earlier than the current time, add one day to the date
            if message_datetime < now:
                message_datetime += timedelta(days=1)

            # Calculate the time until the message should be sent
            time_until_message = message_datetime - now

            # Sleep until message is to be sent
            time.sleep(time_until_message.total_seconds())

            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                    smtp.starttls()  # encryption method
                    smtp.login(self.sender_email, self.sender_password)
                    smtp.sendmail(self.sender_email,
                                  self.recipient_email, msg.as_string())
                    print("Message Sent!")
            except Exception as e:
                print(f"Error trying to establish connection - {e}")
            finally:
                print("Process Completed")


if __name__ == "__main__":
    email_client = SMTPAutomator()
    email_client.run()

    process_name = "stmp_quote_to_self"
    setproctitle.setproctitle(process_name)
    # check how many instances of this process is running
    output = subprocess.check_output(
        f"/bin/ps -ef|/bin/grep -v grep|grep-v '/bin/sh'|/bin/grep -c {process_name}", shell=True)

    print(output)
    if output != 1:  # if more than one process, exit
        exit()
