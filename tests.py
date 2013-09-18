import unittest
from smtphandler_backport import SMTPHandler
import mock
import uuid

default_args = ['localhost',
                'from@here.com',
                'to@here.com',
                'this is a test email!?']

class SMTPHandlerTests(unittest.TestCase):

    @mock.patch('smtplib.SMTP')
    def test_emit_sends_email(self, smtp):
        handler = SMTPHandler(*default_args)
        log_string = str(uuid.uuid4())
        handler.emit(log_string)

        server = smtp.return_value
        self.failUnlessEqual(server.sendmail.call_count, 1)
        call_args = server.sendmail.call_args_list[0][0]
        self.failUnlessEqual(call_args[0], default_args[1])
        self.failUnlessEqual(call_args[1], default_args[2])
        email = call_args[2]
        self.failUnless(log_string in email)


    @mock.patch('smtplib.SMTP')
    def test_get_subject(self, smtp):
        subject = str(uuid.uuid4())

        class SubjectSMTPHandler(SMTPHandler):
            def getSubject(self, record):
                return subject

        handler = SubjectSMTPHandler(*default_args)
        handler.emit(str(uuid.uuid4()))
        server = smtp.return_value
        self.failUnlessEqual(server.sendmail.call_count, 1)
        email = server.sendmail.call_args_list[0][0][2]
        self.failUnless('subject: ' + subject in email)


    @mock.patch('smtplib.SMTP')
    def test_security(self, smtp):
        args = default_args[:]
        args.append(('uname', 'pwd'))
        handler = SMTPHandler(*args)
        log_string = str(uuid.uuid4())
        handler.emit(log_string)

        server = smtp.return_value
        self.failUnlessEqual(server.login.call_count, 1)
        self.failUnlessEqual(server.login.call_args_list[0][0][0],
                             'uname')
        self.failUnlessEqual(server.login.call_args_list[0][0][1],
                             'pwd')

if __name__ == "__main__":
    unittest.main()
