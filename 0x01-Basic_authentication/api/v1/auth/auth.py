#!/usr/bin/env python3
""" auth script for the class Auth"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class definition to manage API auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which routes don't need authentication"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if path in excluded_paths or path + "/" in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ validate all requests to secure the API:"""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ return None for now"""
        return None
