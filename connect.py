#!/usr/bin/python
import psycopg2
import yagmail
from config import config


def connect_db():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config(section='postgresql')

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        return conn;
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def connect_gmail(subject, contents, filename):
    """ yagmail is a GMAIL/SMTP client that aims to make it as simple as possible to send emails."""
    # read connection parameters
    params = config(section='gmail')
    yag = yagmail.SMTP(params['sender'], params['password'])
    yag.send(
        to=params['receiver'],
        subject=subject,
        contents=contents,
        attachments=filename
    )
