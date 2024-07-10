#!/usr/bin/env python3
""" basic_auth script for the class BasicAuth"""

from flask import request
from typing import List, TypeVar
from .auth import Auth
import base64
from models.user import User
from models.base import DATA


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth class"""
    def extract_base64_authorization_header(
                self, authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header
            for a Basic Authentication"""
        if authorization_header is None or not isinstance(
                authorization_header, str) or\
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64 string """
        if base64_authorization_header is None or not isinstance(
             base64_authorization_header, str):
            return None
        try:
            encoded_utf = base64_authorization_header.encode("utf-8")
            base64_decoded = base64.b64decode(encoded_utf)
            return base64_decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None or\
            not isinstance(decoded_base64_authorization_header, str) or\
                ":" not in decoded_base64_authorization_header:
            return None, None
        [user, password] = decoded_base64_authorization_header.split(":")
        return user, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """ returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        User.load_from_file()
        if 'User' not in DATA.keys() or not DATA:
            return None

        usr_found = User.search({"email": user_email})
        if not usr_found:
            return None
        if not usr_found[0].is_valid_password(user_pwd):
            return None

        return usr_found[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        extracted_b64 = self.extract_base64_authorization_header(auth_header)
        decoded_b64 = self.decode_base64_authorization_header(extracted_b64)
        user, password = self.extract_user_credentials(decoded_b64)
        return self.user_object_from_credentials(user, password)
