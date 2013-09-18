import unittest
from smtphandler_backport import SMTPHandler
import mock
import uuid
import logging

default_args = ['localhost',
                'from@here.com',
                'to@here.com',
                'this is a test email!?']


class SMTPHandlerTests(unittest.TestCase):

    @mock.patch('smtplib.SMTP')
    def test_emit_sends_email(self, smtp):
        handler = SMTPHandler(*default_args)
        log_string = str(uuid.uuid4())
        handler.emit(logging.LogRecord('', logging.DEBUG, '', 0, log_string, [], None))

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
        handler.emit(logging.LogRecord('', logging.DEBUG, '', 0, str(uuid.uuid4()), [], None))

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
        handler.emit(logging.LogRecord('', logging.DEBUG, '', 0, log_string, [], None))

        server = smtp.return_value
        self.failUnlessEqual(server.login.call_count, 1)
        self.failUnlessEqual(server.login.call_args_list[0][0][0],
                             'uname')
        self.failUnlessEqual(server.login.call_args_list[0][0][1],
                             'pwd')


    @mock.patch('smtplib.SMTP')
    def test_logging(self, smtp):
        logger = logging.getLogger('test')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(SMTPHandler(*default_args))
        info_log = str(uuid.uuid4())
        logger.info(info_log)

        server = smtp.return_value
        self.failUnlessEqual(server.sendmail.call_count, 1)
        call_args = server.sendmail.call_args_list[0][0]
        self.failUnless(info_log in call_args[2])


if __name__ == "__main__":
    unittest.main()
