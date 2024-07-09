#!/usr/bin/env python3
""" auth script for the class Auth"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class definition to manage API auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False for now"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if path in excluded_paths or path + "/" in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns None for now"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return None for now"""
        return None
