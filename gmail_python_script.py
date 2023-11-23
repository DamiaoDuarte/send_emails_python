import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
import schedule
import time
from pwd import password


# Define the HTML document
html = '''
    <html>
        <body>
          
            <p>your_tittle_here</p>
            <p>Your_Message_here</p>             
            
        </body>
    </html>
    '''

# Define a function to attach files as MIMEApplication to the email
def attach_file_to_email(email_message, location):
    with open(location, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    # Add header/name to the attachments
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {location}",
    )
    # Attach the file to the message
    email_message.attach(file_attachment)


# Set up the email addresses and password. Please replace below with your email address and password
email_from = 'source_email'
password = password
email_to = 'destination_email'

# Generate today's date to be included in the email Subject
date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

# Create a MIMEMultipart class, and set up the From, To, Subject fields
while True:
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'Your_subject_here'

# Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))

# Attach more (documents)
# Just add the full path of the file.
    attach_file_to_email(
        email_message, r"your_path_here\test.pdf")
    attach_file_to_email(
        email_message, r"your_path_here\test.txt")

# Convert it as a string
    email_string = email_message.as_string()

# Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string)

    print("Email has been sent successfully!!!")

# wait for 30 minutes
    time.sleep(30 * 60)
