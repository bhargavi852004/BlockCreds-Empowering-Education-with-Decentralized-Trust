import os
from django.core.mail import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")


def send_certificate_email(student_email: str, student_name: str, certificate_path: str, qr_path: str):
    """
    Send an email with certificate and optional QR code attached.
    """
    if not EMAIL_HOST_USER:
        raise ValueError("❌ EMAIL_HOST_USER not set in .env")

    subject = "Your Certificate is Ready"
    body = f"""
    Hello {student_name},

    🎉 Congratulations! Your certificate has been generated and verified on blockchain.

    You can find it attached to this email.

    Regards,  
    Educhain Team
    """

    email = EmailMessage(subject, body, EMAIL_HOST_USER, [student_email])
    email.attach_file(certificate_path)

    if qr_path and os.path.exists(qr_path):
        email.attach_file(qr_path)

    email.send()
