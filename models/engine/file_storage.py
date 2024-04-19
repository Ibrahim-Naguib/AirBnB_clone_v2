#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import shlex
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage
        Args:
            cls: class name
        """
        if cls is None:
            return self.__objects
        else:
            className = cls if isinstance(cls, str) else cls.__name__
            result_all = {}
            for key, value in self.__objects.items():
                if key.split('.')[0] == className:
                    result_all[key] = value
            return result_all

    def new(self, obj):
        """Adds new object to storage dictionary
        Args:
            obj: instance object
        """
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        new_dict = {}
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict().copy()

        with open(self.__file_path, mode="w", encoding="utf-8") as my_file:
            json.dump(new_dict, my_file)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
            for obj in temp.values():
                cls_name = obj['__class__']
                del obj['__class__']
                class_gl = globals()[cls_name]
                inst = class_gl(**obj)
                self.new(inst)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ delete an existing element from __objects
        Args:
            obj: object
        """
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """method for deserializing the JSON file to objects"""
        self.reload()
