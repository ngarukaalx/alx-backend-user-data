#!/usr/bin/env python3
"""This module contains SessionAuth"""
from api.v1.auth.auth import Auth
import uuid
from flask import request


class SessionAuth(Auth):
    """for creating a new authentication mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        from models.user import User
        # retrive the sesionId
        cookie_sessionid = super().session_cookie(request)
        # get the user id
        user_id = self.user_id_for_session_id(cookie_sessionid)
        # get user instance
        user_instance = User.get(user_id)
        return user_instance

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        session_id = super().session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        del self.user_id_by_session_id[session_id]
        return True
