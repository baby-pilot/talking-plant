"""
Sends SMS with MS outlet email
ADD a settings.py file with:
SENDER_EMAIL_PASSWORD: your email password
SENDER_EMAIL: your email address
CARRIER: google the domain of your carrier (see dict below)
RECEIVER_NUMBER: your phone number

CARRIER_MAP = {
    "verizon": "vtext.com",
    "tmobile": "tmomail.net",
    "sprint": "messaging.sprintpcs.com",
    "at&t": "txt.att.net",
    "boost": "smsmyboostmobile.com",
    "cricket": "sms.cricketwireless.net",
    "uscellular": "email.uscc.net",
}

Source: https://stackoverflow.com/questions/62476801/sending-sms-texts-in-python-without-the-need-for-a-3rd-party-api
code adapted from: https://github.com/acamso/demos/blob/master/_email/send_txt_msg.py
"""

from email.message import EmailMessage
from typing import Tuple, Union
import settings  # makeshift env file

import smtplib

# docs: https://pypi.org/project/aiosmtplib/

# does not work with illinois.edu --
# Use your personal outlook/hotmail account with an app password if you have 2FA enabled
HOST = "smtp-mail.outlook.com"


def send_txt(
    msg: str, subj: str = "Your Plant", num: Union[str, int] = settings.RECEIVER_NUMBER
):

    # set up sender email
    to_email = settings.CARRIER
    email = settings.SENDER_EMAIL
    pword = settings.SENDER_EMAIL_PASSWORD

    # build message
    message = EmailMessage()
    message["From"] = email
    message["To"] = f"{num}@{to_email}"
    message["Subject"] = subj  # subject appears within parenthesis in text message
    message.set_content(msg)

    # Send
    try:
        with smtplib.SMTP(HOST, 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(email, pword)  # Log in to the SMTP server
            server.send_message(message)  # Send the email
        msg = "SMS alert sent successfully"
    except smtplib.SMTPException as e:
        msg = f"failed due to {str(e)}"

    print(msg)


if __name__ == "__main__":
    _msg = "Dummy msg"
    _subj = "Dummy subj"
    coro = send_txt(_msg, _subj)
