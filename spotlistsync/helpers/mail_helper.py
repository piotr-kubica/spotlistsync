import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from spotlistsync.helpers.logger_helper import get_logger
from spotlistsync.config import Config  # type: ignore


logger = get_logger(__name__)


class GMailSender:
    default_retry = 2
    default_retry_sleep = 30
    default_timeout = 15

    def __init__(self, conf: Config) -> None:
        self.gmail_user = conf['mail']['user']
        self.gmail_pass = conf['mail']['pass']

    def send_email(self, topic="", message="", recepient=""):
        to = recepient
        bcc = cc = ''
        msg = self._create_message(topic, message, recepient, cc)
        self._send(msg, self.gmail_user, to, cc, bcc)
            
    def _create_message(self, topic, message, recepient, cc):
        sent_from = self.gmail_user
        subject = topic
        send_to = [recepient]
        send_cc = [cc]

        # create message - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] =  subject
        msg['From'] = sent_from
        msg['To'] = ", ".join(send_to)
        msg['cc'] = ", ".join(send_cc)
        text = message
        mime_text = MIMEText(text, 'plain')
        msg.attach(mime_text)
        return msg

    def _send(self, msg, _from, to, cc, bcc):
        retry = initial_retry_cnt = self.default_retry
        while(retry > 0):
            try:
                logger.info("Sending message: " + msg.as_string())
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465, None, None, None, timeout=10)
                server.ehlo()
                server.login(self.gmail_user, self.gmail_pass)
                server.sendmail(_from, to + cc + bcc, msg.as_string())
                server.close()
                logger.info("Message sent successfully!")
                retry = 0
            except OSError as ex:
                logger.info("Message failed to send! Reason: " + str(ex))
                retry -= 1
                logger.info("Retry " + str(initial_retry_cnt - retry) + " of " + str(initial_retry_cnt))
                time.sleep(self.default_retry_sleep)