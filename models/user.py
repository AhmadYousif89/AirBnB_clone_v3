#!/usr/bin/python3
"""Module for User class"""
import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage_type


class User(BaseModel, Base):
    """Representation of a user"""

    if storage_type == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column("password", String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship("Place", backref="user", cascade="all, delete")
        reviews = relationship("Review", backref="user", cascade="all, delete")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        """Returns the password of the user"""
        return self._password

    @password.setter
    def password(self, value):
        """Hashing password values using md5 hash function"""
        self._password = hashlib.md5(str(value).encode()).hexdigest()
