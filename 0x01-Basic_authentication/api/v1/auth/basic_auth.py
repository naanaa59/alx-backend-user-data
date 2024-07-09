#!/usr/bin/env python3
""" basic_auth script for the class BasicAuth"""

from flask import request
from typing import List, TypeVar
from .auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth class"""
    def extract_base64_authorization_header(
                self, authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header
            for a Basic Authentication"""
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            # print(authorization_header.startswith('Basic '))
            return None
        return authorization_header[6:]