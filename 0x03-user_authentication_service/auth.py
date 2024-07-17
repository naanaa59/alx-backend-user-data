#!/usr/bin/env python3
""" auth script defines _hash_password method for now """
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ hashes a password using bcrypt.hashpw"""
    bytes = password.encode("utf-8")

    salt = gensalt()

    hash = hashpw(bytes, salt)
    return(hash)


def _generate_uuid() -> str:
    """ returns a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ save a user, if does'nt exist, with hashed password"""
        hashed_pwd = _hash_password(password)
        try:
            usr = self._db.find_user_by(email=email)
            if usr is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(email=email, hashed_password=hashed_pwd)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ checks credentials validation"""
        try:
            usr = self._db.find_user_by(email=email)
            if usr is not None:
                return checkpw(password.encode('utf-8'), usr.hashed_password)
        except NoResultFound:
            return False
        return False
