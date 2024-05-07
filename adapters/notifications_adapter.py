import os
import ssl
import smtplib
from typing import Any
from email.message import EmailMessage
from domain.notifications_interface import INotifications

class notifications_adapter(INotifications):

    def send_notification(notifaction: dict) -> None:
        email_sender = 'matiascavallin96@gmail.com'
        subject = 'Nueva venta realizada'
        body_seller = 'Se ha realizado una nueva compra con al menos uno de tus productos'
        body_user = 'Usted ha realizado una nueva compra'

        for email_seller in notifaction['email_seller']:
            em_seller = notifications_adapter.create_email(email_sender, email_seller, subject, body_seller)
            notifications_adapter.send_email(email_sender, email_seller, em_seller)

        em_user = notifications_adapter.create_email(email_sender, notifaction['email_user'], subject, body_user)
        notifications_adapter.send_email(email_sender, notifaction['email_user'], em_user)
        
        return NotImplemented
    
    def create_email(email_sender: str, email_receiver: str, subject: str, body: str) -> EmailMessage:
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        return em
    
    def send_email(email_sender:str, email_receiver: str, em: EmailMessage) -> None:
        context = ssl.create_default_context()
        password = os.getenv('GMAIL_PW')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            smtp.quit()
    