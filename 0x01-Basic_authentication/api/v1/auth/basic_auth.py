#!/usr/bin/env python3
""" basic_auth script for the class BasicAuth"""

from flask import request
from typing import List, TypeVar
from .auth import Auth
import base64


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
