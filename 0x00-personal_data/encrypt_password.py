#!/usr/bin/env python3
"""the module has func hash_password that
returns a salted hashed password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password,
    which is a byte string
    """
    passw = password.encode('utf-8')
    hashed = bcrypt.hashpw(passw, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if encripted password match str password"""
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)
