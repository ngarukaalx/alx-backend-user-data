#!/usr/bin/env python3
"""class BasicAuth that inherits from"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar


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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """returns the user email and password from the Base64
        decoded value
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        pass_email = decoded_base64_authorization_header.split(':', maxsplit=1)
        return pass_email[0], pass_email[1]

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        from models.user import User
        if user_email is None or not isinstance(user_email, str) or\
                user_pwd is None or not isinstance(user_pwd, str):
            return None
        # get the instance
        instance = User.search(attributes={"email": user_email})
        # return None if database doesn't contain any instance
        if len(instance) < 1:
            return None
        # check if password is valid for the instance
        is_valid = instance[0].is_valid_password(user_pwd)
        if not is_valid:
            return None
        return instance[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance
        for a request
        """
        if request:
            header = super().authorization_header(request)
            auth_header = self.extract_base64_authorization_header(header)
            decoded_header = self.decode_base64_authorization_header(
                    auth_header
                    )
            cridentials = self.extract_user_credentials(decoded_header)
            user_instance = self.user_object_from_credentials(
                    cridentials[0],
                    cridentials[1]
                    )
            return user_instance
        return None
