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

    def create_session(self, email: str) -> str:
        """ create a user session of a created user and return it"""
        try:
            usr = self._db.find_user_by(email=email)
            if usr is not None:
                session_id = _generate_uuid()
                usr.session_id = session_id
                # self._db.update_user(usr.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None
        return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ return a user based on a session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ updates the corresponding user's session Id to None"""
        try:
            self._db.update_user(user_id, session_id=None)
            # print("///")
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ Find the user correspondind to the email, generate a UUID
        and update the users's reset_token , retrn token
        """
        try:
            usr = self._db.find_user_by(email=email)
            if usr is not None:
                usr.reset_token = _generate_uuid()
                return usr.reset_token
        except NoResultFound:
            raise ValueError
        return None

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates the user's password by updating hashed_password and
        destroying reset_token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            setattr(user, "hashed_password", hashed_pwd)
            setattr(user, "reset_token", None)
        except NoResultFound:
            raise ValueError
        return None
