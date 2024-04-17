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
        for val in excluded_paths:
            pattern = val.split('/')
            path = path.split('/')
            if re.match(pattern[-1], path[-1]):
                return False
        return False

    def authorization_header(self, request=None) -> str:
        """returns None """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """returns none"""
        return None
