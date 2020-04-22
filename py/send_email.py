#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:09:54 2020

@author: root
"""

import json
import smtplib, ssl
import pandas as pd
from email.message import EmailMessage
import re

def send_emails(data, sender_email, password):
    data = pd.DataFrame.from_records(data)    
    
    port = 587  # For starttls
    smtp_server = "smtp.gmail.COM"
 
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.connect('smtp.gmail.com', '587')
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
    
        for x in data.employee_name.unique():
            tmp = data.query("employee_name == '{0}'".format(x))
            receiver_name = tmp.employee_name.unique()[0]
            receiver_email = tmp.employee_email.unique()[0]
            
            print(receiver_name)
            # Create the container email message.
            msg = EmailMessage()
            msg['Subject'] = 'Upcoming Schedule'
            msg['From'] = sender_email
            msg['To'] = receiver_email
            message = """\
            Hi there, {0}
            You are scheduled for the following shifts:       
            """.format(receiver_name)
            message = re.sub('    ','',message)
            for idx, row in tmp.iterrows():
                shift_row = '{0} {1} from {2} to {3}\n'.format(row['day_of_week'], 
                                                               row['start'][0:10],
                                                               row['start_hour'], 
                                                               row['end_hour'])
                message = message + shift_row

            msg.set_content(message)
            server.send_message(msg)


with open('/Users/alexlamb/Desktop/Schedule_Opt/data.txt') as json_file:
    data = json.load(json_file)

send_emails(data, sender_email, password)


