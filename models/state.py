#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City
import models

storage_type = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class to store state information
    Attributes:
        name: input name
    """
    if storage_type == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete, delete-orphan',
                              backref='state')
	else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if storage_type != 'db':
        @property
        def cities(self):
            """returns the list of City instances with state_id"""
            state_cities = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    state_cities.append(city)
            return state_cities
