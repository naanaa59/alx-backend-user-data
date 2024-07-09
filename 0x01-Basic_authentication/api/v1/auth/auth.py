#!/usr/bin/env python3
""" auth script for the class Auth"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class definition to manage API auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False for now"""
        return False

    def authorization_header(self, request=None) -> str:
        """ returns None for now"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return None for now"""
        return None
