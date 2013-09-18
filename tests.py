import unittest
from smtphandler_backport import SMTPHandler
import mock

class SMTPHandlerTests(unittest.TestCase):

    @mock.patch('smtplib.SMTP')
    def test_emit_sends_email(self, smtp):
        handler = SMTPHandler('localhost',
                              'from@here.com',
                              'to@here.com',
                              'this is a test email!?')
        handler.emit("BLAH")

    def test_get_subject(self):
        pass


if __name__ == "__main__":
    unittest.main()
