#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage
import shlex


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade='all, delete, delete-orphan',
                          backref='state')

    @property
    def cities(self):
        all_objs = storage.all()
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
