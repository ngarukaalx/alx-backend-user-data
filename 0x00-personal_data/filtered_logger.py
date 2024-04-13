#!/usr/bin/env python3
"""This module contains filter_datum function"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log msg obfuscated"""
    msg_copy = message
    for field in fields:
        pattern = r'(\b{}\s*=\s*)([^{}]*)(?=;)'.format(re.escape(field),
                                                       re.escape(separator))
        new_string = re.sub(pattern, r'\1' + redaction, msg_copy)
        msg_copy = new_string
    return msg_copy
