#!/usr/bin/env python3
"""This module comtains DB class"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Any, Dict

from user import User, Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add_user method and returns the added object"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Returns the first row found inthe user
        table as filtered by the methods input
        """
        query = self._session.query(User)
        for key, value in kwargs.items():
            try:
                query = query.filter(getattr(User, key) == value)
            except AttributeError:
                raise InvalidRequestError()
        user = query.first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates the user object with provided **kwargs"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            try:
                if not hasattr(user, key):
                    raise ValueError()
                setattr(user, key, value)
            except AttributeError:
                raise ValueError()
        self._session.commit()
