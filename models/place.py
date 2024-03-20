#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
import models
from os import getenv
from models.amenity import Amenity
from models.review import Review


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             nullable=False, primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             nullable=False, primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: description of the input
        number_rooms: number of rooms
        number_bathrooms: number of bathrooms
        max_guest: maximum guest
        price_by_night: pice for a staying
        latitude: latitude of the place
        longitude: longitude of the place
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', cascade='all, delete, delete-orphan',
                               backref='place')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False,
                                 back_populates='place_amenities')
    else:
        @property
        def reviews(self):
            """returns a list of Review instances"""
            return [review for review in models.storage.all(Review).values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """returns a list of Amenity instances"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """sets the list of Amenity instances"""
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
