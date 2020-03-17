from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMessage
from cakeshop.celery import app


@app.task
def task_sendmail(subject, message, email_from, recipient_list):
    message = EmailMessage(subject, message, email_from, recipient_list)
    message.attach_file('/home/kobey/Desktop/mypdf.pdf')
    message.send()


@app.task
def add(x, y):
    time.sleep(5)
    return x + y
