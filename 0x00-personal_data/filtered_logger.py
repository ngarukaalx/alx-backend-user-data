#!/usr/bin/env python3
"""This module contains filter_datum function"""
import re
from typing import List
import logging
from logging import Logger


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
    """rturns a logging.logger object"""
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
