from email.MIMEText import MIMEText
import smtplib


class SMTPHandler(object):

    def __init__(self, mailhost, fromaddr, toaddrs,
                 subject, credentials=None, secure=None):
        self.mailhost = mailhost
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.smtp_username, self.smtp_password = credentials
        self.secure = secure


    def create_email(self, subject, content):
        email = MIMEText(content)
        email.set_type('text/plain')
        email.set_param('charset', 'ASCII')
        email['subject'] = subject
        email['From'] = self.fromaddr
        email['To'] = self.toaddrs
        return email


    def send_mail(self, email):
        server = smtplib.SMTP(self.mailhost)
        if self.secure:
            server.ehlo()
            server.starttls()
            server.ehlo()
        if self.smtp_username:
            assert self.smtp_password
            server.login(self.smtp_username, self.smtp_password)
        server.sendmail(self.fromaddr,
                        self.toaddrs,
                        email.as_string())
        try:
            server.quit()
        except sslerror:
            pass


    def emit(self, record):
        mail = self.create_email(self.subject, record)
        self.send_mail(mail)
