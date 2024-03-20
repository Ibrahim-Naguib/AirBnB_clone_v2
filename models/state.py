#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import shlex
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

    @property
    def cities(self):
        all_objs = models.storage.all()
        city_list = []
        city_rel = []
        for obj in all_objs:
            city = obj.replace('.', ' ')
            city = shlex.split(city)
            if city[0] == 'City':
                city_list.append(city_list[obj])

        for city in city_list:
            if city.state_id == self.id:
                city_rel.append(city)
        return city_rel
