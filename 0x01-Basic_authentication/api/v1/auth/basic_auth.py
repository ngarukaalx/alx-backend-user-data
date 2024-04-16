#!/usr/bin/env python3
"""class BasicAuth that inherits from"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """class BasicAuth that inheritss from Auth"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is \
                None or not isinstance(authorization_header, str) \
                or not authorization_header.startswith("Basic "):
            return None
        # split the string into words
        after_basic = authorization_header.split()
        return after_basic[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """Returns decoded value of base64 string"""
        if base64_authorization_header is \
                None or not isinstance(base64_authorization_header, str):
            return None
        # converting to bytes
        try:
            encoded_data = base64.b64decode(base64_authorization_header)
            return encoded_data.decode('utf-8')
        except Exception:
            return None
