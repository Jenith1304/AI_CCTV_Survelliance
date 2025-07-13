# email_utils.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.extensions import mongo
from bson import ObjectId
def get_email_settings(user):
    config = mongo.db.email_config.find_one({"user_id": ObjectId(user)})
    if not config:
        raise ValueError("Email configuration not set.")
    return config

def send_alert_email(user, detections=[], zones=[]):
    try:
        config = get_email_settings(user)
    except ValueError as e:
        print("[EMAIL ERROR]", e)
        return

    subject = "[ALERT] Helmet or Zone Violation Detected"
    messages = []

    if "No Helmet" in detections:
        messages.append("🚨 A person without a helmet was detected.")
    for zone in zones:
        messages.append(f"⚠️ Zone unattended: {zone}")

    if not messages:
        return

    body = "\n".join(messages)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = config["sender"]
    msg['To'] = config["receiver"]
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(config["sender"], config["app_password"])
            smtp.send_message(msg)
        print(f"[EMAIL SENT] {subject}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
