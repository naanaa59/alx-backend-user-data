#!/usr/bin/env python3
""" This script defines multiple functions that deals with personal data """

import logging
from typing import List, Optional
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
    fields in the log line (message)
    return:  the log message obfuscated
    """
    for field in fields:
        pattern = rf'{re.escape(field)}=.*?(?={re.escape(separator)}|$)'
        message = re.sub(pattern, rf'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Custum logging formatter that obfuscates certain fields in msg"""
        message = super(RedactingFormatter, self).format(record)
        message = filter_datum(self.fields, self.REDACTION, message,
                               self.SEPARATOR)

        return message
