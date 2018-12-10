# coding:utf-8
import csv
import os
import smtplib

from collections import namedtuple
from datetime import datetime
from random import shuffle


EMAIL_TEMPLATE = 'email_template.txt'
SANTAS_FILE = 'santas.txt'
MAILER_ACCOUNT_EMAIL = 'SANTA_MAILER_ACCOUNT_EMAIL'
MAILER_ACCOUNT_TOKEN = 'SANTA_MAILER_ACCOUNT_TOKEN'
MAILER_SIGNOFF_NAME = 'SANTA_EMAIL_SIGNOFF_NAME'

SantaInfo = namedtuple('SantaInfo', ['email', 'name'])
MailerCredentials = namedtuple('MailerCredentials', ['email', 'token'])


class SecretSanta(object):
    """
    A fun, lightweight script to automate the selection process of the
    Secret Santa holiday event.

    Public:
        kickoff(): entrypoint to match and email the secret santas.

    Instance Attributes:
        email:              stores the email template that is loaded from a
                            file.
        email_signoff_name: name used at bottom of email template for signoff
                            signature.
        mailer_creds:       a MailerCredentials namedtuple that stores the
                            secrets for the email account that will deliver our
                            event emails.
        santas:             list(SantaInfo) - name and email of all
                            participating santas.
        giftees:            list(string) - names to be assigned to a santa.
    """
    def __init__(self):
        self.email = self._load_email_template(EMAIL_TEMPLATE)
        self.santas = []
        self.giftees = []
        self._load_settings_from_env()

    def kickoff(self):
        """
        Fires off a round of matching all secret santas with a giftee then
        notifies the santas by email.
        """
        self._create_santa_giftee_lists(SANTAS_FILE)
        self._email_all_santas()

    def _load_email_template(self, template):
        """
        Load email template from disk.

        :param template: filename in path format.
        """
        print('Loading email template...')

        with open(template) as file:
            email = file.read()

        return email

    def _load_mailer_credentials_from_env(self):
        """
        Load the email account secrets that we will use to send our santa
        emails from env variables.

        :return MailerCredentials: tuple(email, token)
        """
        print('Loading email credentials from env...')

        account_creds = {}
        for key, value in os.environ.items():
            if key == MAILER_ACCOUNT_EMAIL:
                account_creds['email'] = value
            if key == MAILER_ACCOUNT_TOKEN:
                account_creds['token'] = value

        return MailerCredentials(**account_creds)

    def _load_settings_from_env(self):
        """
        Sets script settings from env variables.
        """
        self.mailer_creds = self._load_mailer_credentials_from_env()
        print('Loading signoff name from env...')
        self.email_signoff_name = os.environ.get(MAILER_SIGNOFF_NAME)

    def _create_santa_giftee_lists(self, santas_list):
        """
        Loads the list of our santa participants from disk then generates a
        list of secret santas. Also generates and shuffles a list of giftees
        from the secret santas.

        :param santas_list: filename in path format.
        """
        print('Loading santas and creating giftees...')
        self.santas = []
        self.giftees = []

        with open(santas_list) as santa_file:
            csv_reader = csv.DictReader(santa_file, delimiter=' ')

            for santa_row in csv_reader:
                santa_info = SantaInfo(**santa_row)

                self.giftees.append( santa_info.name )
                self.santas.append( santa_info )

        shuffle(self.giftees)

    def _send_email(self, conn, santa, giftee):
        """
        Send an email to inform our secret santa who they will be gifting.

        :param conn: the connection to the email server.
        :param santa: SantaInfo for the secret santa.
        :param giftee: the name of the person the santa will gift.
        """
        print('Sending santa email for: {santa}'.format(santa=santa.name))

        msg = self.email.format(
            to_email=santa.email,
            year=datetime.now().year,
            santa=santa.name,
            giftee=giftee,
            signoff_name=self.email_signoff_name
        )
        conn.sendmail(self.mailer_creds.email, [santa.email], msg)

    def _email_all_santas(self):
        """
        Opens an SMTP connection, logs in our mailer account and emails each
        santa.
        """
        print('Logging into gmail account...')

        with smtplib.SMTP('smtp.gmail.com', 587) as es:
            es.starttls()
            es.login(self.mailer_creds.email, self.mailer_creds.token)

            for santa_info in self.santas:
                found = False
                i = 0
                while not found:
                    # a santa cannot gift themself.
                    giftee = self.giftees[i]
                    if giftee != santa_info.name:
                        found = True
                        self._send_email(es, santa_info, giftee)
                        # shrink list once a match is made.
                        self.giftees.remove(giftee)
                    else:
                        i += 1


if __name__ == '__main__':
    santa = SecretSanta()
    santa.kickoff()
