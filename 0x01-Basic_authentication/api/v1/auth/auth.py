#!/usr/bin/env python3
"""class to manage the API authetication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage API authetication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false"""
        if path is not None and path[-1] != '/':
            path = path + '/'
        if path is None or excluded_paths is None \
                or len(excluded_paths) < 1 or path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """returns None """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns none"""
        return None
