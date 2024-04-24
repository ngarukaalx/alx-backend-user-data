#!/usr/bin/env python3
"""This module contains _hash_password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union, Optional


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

    def create_session(self, email: str) -> str:
        """create session id and save it to the database
        returns the session_id after udtating the user"""
        try:
            user = self._db.find_user_by(email=email)
            session = _generate_uuid()
            self._db.update_user(user.id, session_id=session)
            return session
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """find user by session id"""
        if session_id is None:
            return None
        try:
            # check if user exists
            user = self._db.find_user_by(session_id=session_id)
            return user
        except InvalidRequestError:
            return None
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError:
            return None
