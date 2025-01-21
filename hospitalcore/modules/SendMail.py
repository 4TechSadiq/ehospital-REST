import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO

def send_invoice_email(pdf_buffer, recipient_email, subject, body, sender_email, sender_password):
    """
    Sends an email with the attached PDF invoice.

    Args:
        pdf_buffer (BytesIO): The PDF file in memory.
        recipient_email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body text of the email.
        sender_email (str): The sender's email address.
        sender_password (str): The sender's email password.

    Returns:
        None
    """
    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_buffer.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="Medical_Invoice.pdf"')
    msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")