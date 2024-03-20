#!/usr/bin/python3
"""This module defines a class to manage Database storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages Database storage
    Attributes:
        __engine: engine
        __session: session
    """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a new model"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in Database
        Args:
            cls: class name
        """
        all_classes = {
            "State": State,
            "City": City,
            "User": User,
            "Place": Place,
            "Review": Review,
            "Amenity": Amenity,
        }
        new_dict = {}
        for clss in all_classes:
            if cls is None or cls is all_classes[clss] or cls is clss:
                objs = self.__session.query(all_classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """Adds the object to the current database session
        Args:
            obj: instance object
        """
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session
        Args:
            obj: instance object
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """Closes the current database session"""
        self.__session.close()
