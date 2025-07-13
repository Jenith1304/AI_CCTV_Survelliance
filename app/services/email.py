import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime

def send_alert_email(detections=[], zones=[]):
    sender = os.getenv("ALERT_EMAIL")
    password = os.getenv("ALERT_PASSWORD")
    receiver = os.getenv("ALERT_TO")
    if not sender or not receiver:
        print("[MAIL] Missing credentials")
        return

    subject = "[Alert] Safety Violation Detected"
    messages = []

    if "No Helmet" in detections:
        messages.append("🚨 Person detected without helmet.")
    for z in zones:
        messages.append(f"⚠️ Machine zone unattended: {z}")

    if not messages:
        return

    body = "\n".join(messages)
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print(f"[MAIL] Sent: {body}")
    except Exception as e:
        print(f"[MAIL ERROR] {e}")
