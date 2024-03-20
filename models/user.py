#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes
    Attributes:
        email: email address of the user
        password: password of the user
        first_name: first name of the user
        last_name: last name of the user
    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship('Place', cascade='all, delete, delete-orphan',
                          backref='user')
    reviews = relationship('Review', cascade='all, delete, delete-orphan',
                           backref='user')
