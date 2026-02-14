import smtplib
import re
import os
import mimetypes
from email.message import EmailMessage
from datetime import datetime

# ================= CONFIGURATION =================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "maheshsp1268@gmail.com"
APP_PASSWORD = "tocrfyvtnbmzsqcy"
LOG_FILE = "email_log.txt"


# ================= VALIDATION =================
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def validate_inputs(recipients, subject, body, attachment):
    for email in recipients:
        if not is_valid_email(email):
            return False, f"Invalid email: {email}"

    if not subject.strip():
        return False, "Subject cannot be empty"

    if not body.strip():
        return False, "Email body cannot be empty"

    if attachment and not os.path.exists(attachment):
        return False, "Attachment file not found"

    return True, "Validation successful"


# ================= EMAIL BUILDER =================
def build_email(sender, recipients, subject, body, attachment=None):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment:
        mime_type, _ = mimetypes.guess_type(attachment)
        mime_type, mime_subtype = mime_type.split("/")

        with open(attachment, "rb") as file:
            msg.add_attachment(
                file.read(),
                maintype=mime_type,
                subtype=mime_subtype,
                filename=os.path.basename(attachment)
            )

    return msg


# ================= EMAIL SENDER =================
def send_email(message):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(message)
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)


# ================= LOGGER =================
def log_status(recipients, status, info):
    with open(LOG_FILE, "a") as log:
        for recipient in recipients:
            log.write(
                f"{datetime.now()} | To: {recipient} | Status: {status} | Info: {info}\n"
            )


# ================= MAIN FUNCTION =================
def main():
    print("\n📧 EMAIL SENDER AUTOMATION\n")

    recipients = input("Enter recipient emails (comma separated): ").split(",")
    recipients = [email.strip() for email in recipients]

    subject = input("Enter email subject: ")
    body = input("Enter email message: ")
    attachment = input("Enter attachment path (press Enter to skip): ").strip()

    is_valid, message = validate_inputs(recipients, subject, body, attachment)
    if not is_valid:
        print("❌", message)
        return

    email_message = build_email(
        SENDER_EMAIL,
        recipients,
        subject,
        body,
        attachment if attachment else None
    )

    success, result = send_email(email_message)

    log_status(recipients, "SUCCESS" if success else "FAILED", result)

    if success:
        print("✅ Email sent successfully")
    else:
        print("❌ Email failed:", result)


# ================= PROGRAM START =================
if __name__ == "__main__":
    main()
