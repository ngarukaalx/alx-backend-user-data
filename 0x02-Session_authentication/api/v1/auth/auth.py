#!/usr/bin/env python3
"""class to manage the API authetication"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """class to manage API authetication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false"""
        if path is not None and path[-1] != '/':
            path = path + '/'

        if path is None or excluded_paths is None \
                or len(excluded_paths) < 1:
            return True
        for val in excluded_paths:
            if val.endswith('/'):
                val = val[:-1]
            pattern = val.split('/')
            if path.endswith('/'):
                path = path[:-1]
            path_l = path.split('/')
            if re.match(pattern[-1], path_l[-1]):
                return False
        if path not in excluded_paths:
            return True
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
