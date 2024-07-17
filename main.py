import os
from datetime import date,datetime

import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv

from pyairtable import Api
from apscheduler.schedulers.blocking import BlockingScheduler



PORT=465 #465 for ssl
EMAIL_SERVER="smtp.gmail.com"
context=ssl.create_default_context()


current_dir= Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars=current_dir/ ".env"  # name of env file
load_dotenv(envars)

# create env file and fill the required details
email_sender = os.getenv("EMAIL")
email_password = os.getenv("PASSWORD")


# fetching api
api = Api(os.environ['API'])
base_id='appDQmqX9KileqFCh'   # replace the airtable base id
table_id='tblWa8tXHQJtA6eHZ'  #replace the airtable email id
table = api.table(base_id,table_id)
records=table.all()




def send_email(subject,to_name,email_receiver): 
    msg=EmailMessage()
    msg["Subject"]=subject
    msg["From"]=formataddr(("FOSSCU-KIET",f'{email_sender}')) # change the title of mail
    msg["To"]=email_receiver
    msg["BCC"]=email_sender

    present=date.today()
    email_count=0
    for record in records:
        field=record["fields"]
        date_object = datetime.strptime(field.get("Date"), "%d-%m-%Y").date()

        if (present >= date_object)and(not(field.get("Status")=="sent")):
                subject="subject"
                email_receiver="rvinayak108@gmail.com"  #replace with email whom to send
                name=field.get("Name")
                project=field.get("Project Name")
                link=field.get("Link")
                on_date=field.get("Date")
                msg.set_content(           #correct the email format as requied
                    f'''                          
                        Hi {to_name},
                        We have recent project named {project} by {name} on {on_date}.
                        You can check the project work on github at {link}.
                        ..............
                        .........
                        ..........
                        ..........
                        ...............
                        ..................
                    '''
                )
                try:
                    with smtplib.SMTP_SSL(EMAIL_SERVER, PORT, context=context) as server:
                            server.login(email_sender, email_password)
                            server.sendmail(email_sender, email_receiver, msg.as_string())
                            print("Email sent successfully!")
                except (smtplib.SMTPException, smtplib.SMTPSenderRefused) as error:
                    print(f"Error sending email: {error}")
                email_count+=1
        
    print(f"Total emails sent:{email_count}")




if __name__ == "__main__":
    send_email(
        subject="subject",
        to_name="Gaurav Sir",
        email_receiver="rvinayak108@gmail.com",   #replace with email whom to send
    )