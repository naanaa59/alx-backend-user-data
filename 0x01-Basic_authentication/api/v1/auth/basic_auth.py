#!/usr/bin/env python3
""" basic_auth script for the class BasicAuth"""

from flask import request
from typing import List, TypeVar
from .auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth class"""
