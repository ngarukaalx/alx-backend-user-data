#!/usr/bin/env python3
"""class to manage the API authetication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage API authetication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns None """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns none"""
        return None
