#!/user/bin/env python3
"""This module contains _hash_password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """returns bytes salted hash of the input password"""
    passw = password.encode('utf-8')
    return bcrypt.hashpw(passw, bcrypt.gensalt())
