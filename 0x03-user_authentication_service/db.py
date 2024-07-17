#!/usr/bin/env python3
"""DB module documentations: this module define DB class
"""
from sqlalchemy import create_engine   # type: ignore
from sqlalchemy.ext.declarative import declarative_base   # type: ignore
from sqlalchemy.orm import sessionmaker   # type: ignore
from sqlalchemy.orm.session import Session   # type: ignore
from sqlalchemy.orm.exc import NoResultFound   # type: ignore
from sqlalchemy.exc import InvalidRequestError   # type: ignore
from user import Base
from user import User
from typing import Optional


class DB:
    """DB class defintion: The class where all methods are defined
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ returns a User object and saves the user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **arguments) -> User:
        """ returns the fst row found in the users table as filtered by arg"""
        query = self._session.query(User)
        for arg, val in arguments.items():
            try:
                q_attr = getattr(User, arg)
            except AttributeError:
                raise InvalidRequestError()
            query = query.filter(q_attr == val)
        result = query.first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **arguments) -> None:
        """ updates a user with the passed args"""
        try:
            usr = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError
        for arg, val in arguments.items():
            if hasattr(usr, arg):
                setattr(usr, arg, val)
            else:
                raise ValueError
        self._session.commit()
        return None
