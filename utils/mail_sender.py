import jwt
from datetime import datetime, timedelta,timezone
from configs import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException


class Sender:
    def __init__(self):
        self.sender_email = settings.mail_sender
        self.userName = settings.mail_login
        self.password = settings.mail_password
        self.smtp_port = settings.smtp_port
        self.smtp_server = settings.smtp_server
        self.secret_key = settings.jwt_secret_key  
        
        
  

    def send_mail(self, to,token, subject="Email Verification"):
        if not (to and subject):
            print('Required data is missing')
            return False

        try:
            verification_url = f"{settings.verification_url}{token}"

            # Create the email
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = to

            html = f"""\
                <html>
                <body>
                    <p>Hi,<br>
                    Please verify your email address by clicking the link below:<br>
                    <a href="{verification_url}">Verify Email</a>
                    <br><br>
                    This link will expire in 24 hours.
                    </p>
                </body>
                </html>
                """
            part = MIMEText(html, "html")
            message.attach(part)

            # Connect to SMTP server
            with SMTP(self.smtp_server, self.smtp_port) as server:
                server.login(self.userName, self.password)
                server.sendmail(self.sender_email, to, message.as_string())
                print("Verification email sent successfully.")
                return True

        except SMTPException as ex:
            print(f"SMTP error occurred: {ex}")
            return False
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")
            return False
