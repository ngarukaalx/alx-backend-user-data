#!/usr/bin/env python3
"""this module holds SessionExpAuth"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """class to handle session expiration"""
    def __init__(self):
        """class constructor"""
        sesion_env = os.getenv('SESSION_DURATION')
        to_int = int(sesion_env)
        if not to_int or not sesion_env:
            self.session_duration = 0
        self.session_duration = to_int

    def create_session(self, user_id=None):
        """creates a session id"""
        sesion_id = super().create_session(user_id)
        if not sesion_id:
            return None
        session_dictionary = {}
        session_dictionary["user_id"] = user_id
        session_dictionary["created_at"] = datetime.now()
        super().user_id_by_session_id[sesion_id] = session_dictionary
        return sesion_id

    def user_id_for_session_id(self, session_id=None):
        """returns user_id from session dictionary"""
        if session_id is None:
            return None
        session_value = super().user_id_by_session_id.get(session_id)
        if session_value is None:
            return None
        if self.session_duration <= 0:
            return session_value['user_id']
        created_at = session_value['created_at']
        if created_at is None:
            return None
        total_time = created_at + timedelta(seconds=self.session_duration)
        if total_time < datetime.now():
            return None
        return session_value['user_id']
