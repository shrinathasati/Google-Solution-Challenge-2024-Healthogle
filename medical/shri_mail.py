import smtplib
import ssl
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'YOUR_EMAIL'
email_password = 'YOUR_PASSWORD'
email_receiver = 'RECEIVER_MAIL'

# Set the subject and body of the email
subject = 'Check out my new video!'
body = "Hi i am shrinath"

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())