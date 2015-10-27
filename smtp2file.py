#!/usr/bin/env python3
import smtpd
# import sys
import email
import os
import asyncore
from datetime import datetime
from attachments2file import *


MSGS_DIR = "MSGS"

class SMTP2file(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        mail = email.message_from_string(data)
        print("Received: {}".format(datetime .now()))
        print("From:     {}".format(mailfrom))
        print("To:       {}".format(", ".join(rcpttos)))
        print("Subject:  {}".format(header2str(mail['Subject'])))
        print("Data:")
        print_msg(mail)
        if not os.path.isdir(MSGS_DIR):
            os.makedirs(MSGS_DIR)
        filename = "email_{}.txt".format(datetime.now().strftime("%d_%b_%y_%H-%M-%S_%f"))
        fullfilename = os.path.join(MSGS_DIR, filename)
        with open(fullfilename, "w") as f:
            f.write(data)
            print('msg saved as {}'.format(fullfilename))
        attachments2file(mail, 'attachments')
        print("********END of msg*********")
        
s = SMTP2file(('0.0.0.0', 25), ())
asyncore.loop()
