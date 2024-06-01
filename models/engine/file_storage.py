#!/usr/bin/python3
"""Defines the FileStorage class"""
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "BaseModel": BaseModel,
    "Amenity": Amenity,
    "Review": Review,
    "Place": Place,
    "State": State,
    "City": City,
    "User": User,
}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "hbnb.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is None:
            return self.__objects
        return {
            key: value
            for key, value in self.__objects.items()
            if cls == value.__class__ or cls == value.__class__.__name__
        }

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, 'w') as f:
            json.dump(
                {key: self.__objects[key].to_dict() for key in self.__objects},
                f,
            )

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if not obj:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in self.__objects:
            del self.__objects[key]

    def get(self, cls, id):
        """Retrieve an object based on class and ID"""
        if not cls or not id:
            return
        for clss in classes:
            if cls is classes[clss] or cls == clss:
                key = "{}.{}".format(classes[clss].__name__, id)
                return self.__objects.get(key)

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class"""
        cls = None if cls == "all" else cls
        if cls:
            return len(self.all(cls))
        return len(self.__objects)

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
