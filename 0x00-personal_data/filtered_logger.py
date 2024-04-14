#!/usr/bin/env python3
"""This module contains filter_datum function"""
import re
from typing import List, Optional
import logging
from logging import Logger
from os import getenv
import mysql.connector


PII_FIELDS = ("email", "phone", "ssn", "password", "ip")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log msg obfuscated"""
    for field in fields:
        message = re.sub(f"{field}=(.*?){separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """class constructor takes one args"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum"""
        original_msg = record.getMessage()
        formatted_msg = super(RedactingFormatter, self).format(record)
        new_msg = filter_datum(self.fields, self.REDACTION, formatted_msg,
                               self.SEPARATOR)
        return new_msg


def get_logger() -> Logger:
    """returns a logging.logger object"""
    # create a logger named "user_data"
    logger = logging.getLogger("user_data")
    # set logging level
    logger.setLevel(logging.INFO)
    # set StreamHandler and RedactingFormatter as formatter
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    # add handler to the logger
    logger.addHandler(handler)

    # Disable propagation of log msg to other loggers
    logger.propagate = False
    return logger


def get_db() -> Optional[mysql.connector.connection.MySQLConnection]:
    """returns a connector to the database"""
    PERSONAL_DATA_DB_USERNAME = getenv('PERSONAL_DATA_DB_USERNAME')
    PERSONAL_DATA_DB_PASSWORD = getenv('PERSONAL_DATA_DB_PASSWORD')
    PERSONAL_DATA_DB_HOST = getenv('PERSONAL_DATA_DB_HOST')
    PERSONAL_DATA_DB_NAME = getenv('PERSONAL_DATA_DB_NAME')
    # Establish a connection to the MySQl db
    conn = mysql.connector.connect(
            host=PERSONAL_DATA_DB_HOST,
            user=PERSONAL_DATA_DB_USERNAME,
            password=PERSONAL_DATA_DB_PASSWORD,
            database=PERSONAL_DATA_DB_NAME
            )
    return conn


def main():
    """driver fuction"""
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    column_names = [col[0] for col in cursor.description]

    for row in cursor:
        row_with_names = dict(zip(column_names, row))
        formatted_string = "; ".join(
                [f"{key}={value}" for key, value in row_with_names.items()]
                )
        log_record = logging.LogRecord("user_data",
                                       logging.INFO, None, None,
                                       formatted_string, None, None)
        formatter = RedactingFormatter(fields=("name",
                                       "email", "phone", "ssn", "password"))
        print(formatter.format(log_record))
    connection.close()
    cursor.close()


if __name__ == "__main__":
    """runs only main"""
    main()
