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
        """class constructor initiliazes _db with DB instance"""
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
        """create session id and save it to the database"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

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
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """generate reset password token"""
        try:
            # get the user if exists
            user = self._db.find_user_by(email=email)
            uuid_str = _generate_uuid()
            # update user with reset_ti=oken
            self._db.update_user(user.id, reset_token=uuid_str)
            return uuid_str
        except InvalidRequestError:
            raise ValueError()
        except NoResultFound:
            # raise value error if the user does not exists
            raise ValueError()

    def update_password(self, reset_token: str, password: str):
        """update password using reset_token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pass = _hash_password(password)
            # update user with new password
            self._db.update_user(user.id, hashed_password=hashed_pass)
            self._db.update_user(user.id, reset_token=None)
        except InvalidRequestError:
            raise ValueError()
        except NoResultFound:
            raise ValueError()
