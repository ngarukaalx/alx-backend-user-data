#!/usr/bin/env python3
"""This module contains _hash_password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """returns bytes salted hash of the input password"""
    passw = password.encode('utf-8')
    return bcrypt.hashpw(passw, bcrypt.gensalt())

def _generate_uuid() -> str:
    """returns a string representaion of a new uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """regesters a new user if the email does not exists"""
        if email and password and isinstance(email, str) and\
                isinstance(password, str):
            try:
                # check if user exists
                user = self._db.find_user_by(email=email)
            except NoResultFound:
                hashed_pass = _hash_password(password)
                # save the new user
                user_obj = self._db.add_user(email, hashed_pass)
                return user_obj
            except InvalidRequestError:
                return
            if user is not None:
                raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """credentials validation"""
        # locate the user
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            # check if password match
            password = password.encode('utf-8')
            # check if encripted password match str password
            return bcrypt.checkpw(password, hashed_password)
        except NoResultFound:
            return False
        except InvalidRequestError:
            return False
