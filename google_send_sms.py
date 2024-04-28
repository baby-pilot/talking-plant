import smtplib
from email.message import EmailMessage
from settings import (
    RECEIVER_NUMBER,
    CARRIER,
    SENDER_EMAIL_PASSWORD,
    SENDER_EMAIL,
    CARRIER_MAP,
)

subject = "Email Subject"
body = "This is the body of the text message"


def send_txt(subject, body):
    recipient = f"{RECEIVER_NUMBER}@{CARRIER_MAP[CARRIER]}"

    message = EmailMessage()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
    smtp_server.sendmail(message["From"], [recipient], message.as_string())
    smtp_server.quit()
    print("Message sent!")


if __name__ == "__main__":
    send_txt(subject, body)
