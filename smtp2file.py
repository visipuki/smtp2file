#!/usr/bin/env python3
import smtpd
# import sys
import email
import os
import asyncore
from datetime import datetime
from attachments2file import *


class SMTP2file(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        mail = email.message_from_string(data)
        print("Received: {}".format(datetime.now()))
        print("From:     {}".format(mailfrom))
        print("To:       {}".format(", ".join(rcpttos)))
        print("Subject:  {}".format(header2str(mail['Subject'])))
        print("Data:")
        print_body(mail)
        #msg2file(data, 'MSGS')
        attachments2file(mail, 'attachments')
        print("********END of msg*********")
        
s = SMTP2file(('0.0.0.0', 25), ())
asyncore.loop()
