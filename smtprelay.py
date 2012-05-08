from datetime import datetime
from secure_smtpd  import SMTPServer, FakeCredentialValidator
import asyncore, logging
import sys
import os
import re

SMTPserver = 'mail.hostname.com'
from smtplib import SMTP_SSL as SMTP
USERNAME = "foo"
PASSWORD = "bar"

def send_message(peer, mailfrom, rcpttos, data):
    try:
        conn = SMTP(SMTPserver,port=465)
            #conn.set_debuglevel(True)
            conn.login(USERNAME, PASSWORD)
            try:
                conn.sendmail(mailfrom, rcpttos, data)
            finally:
                conn.close()

        except Exception, exc:
            sys.exit( "mail failed; %s" % str(exc) ) # give a error message

class SMTPForwarder(SMTPServer):
    def __init__(self):
        pass

    def start(self):
        SMTPServer.__init__(self,('10.38.1.18', 25), None,  require_authentication=True, credential_validator=FakeCredentialValidator(), process_count=1)
        asyncore.loop()

    def process_message(self, peer, mailfrom, rcpttos, data):
        send_message(peer, mailfrom, rcpttos, data)

def run():
    foo = SMTPForwarder()
    foo.start()

if __name__ == '__main__':
    run()
