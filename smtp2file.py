#!/usr/bin/env python3
import smtpd
# import sys
import email
import os
import asyncore
from datetime import datetime
from attachments2file import attachments2file, header2str


MSGS_DIR = "MSGS"

class SMTP2file(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        mail = email.message_from_string(data)
        print("Received: {}".format(datetime .now()))
        print("From:     {}".format(mailfrom))
        print("To:       {}".format(", ".join(rcpttos)))
        print("Subject:  {}".format(header2str(mail['Subject'])))
        print("*****************")
        dir = os.curdir + os.path.sep + MSGS_DIR
        if not os.path.isdir(dir):
            os.makedirs(dir)
        filename = "email_{}.txt".format(datetime.now().strftime("%d_%b_%y_%H-%M-%S_%f"))
        fullfilename = os.path.join(dir, os.path.sep, filename)
        with open(fullfilename, "w") as f:
            f.write(data)
        attachments2file(mail, 'attachments')
        
s = SMTP2file(('0.0.0.0', 25), ())
asyncore.loop()
