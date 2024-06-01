#!/usr/bin/python3
"""Defines the DBStorage class"""
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.state import State
from models.user import User

classes = {
    "User": User,
    "City": City,
    "State": State,
    "Place": Place,
    "Review": Review,
    "Amenity": Amenity,
}

ENV = getenv("HBNB_ENV", "dev")
USER = getenv("HBNB_MYSQL_USER", "hbnb_dev")
PWD = getenv("HBNB_MYSQL_PWD", "hbnb_dev_pwd")
HOST = getenv("HBNB_MYSQL_HOST", "localhost")
DB = getenv("HBNB_MYSQL_DB", "hbnb_dev_db")
DB = 'hbnb_test_db' if ENV == 'test' else DB


class DBStorage:
    """interaacts with the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        conn = "mysql+mysqldb://{}:{}@{}/{}"
        self.__engine = create_engine(conn.format(USER, PWD, HOST, DB))
        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls == clss:
                objs = (
                    self.__session.query(classes[clss]).all()
                    if self.__session
                    else []
                )
                for obj in objs:
                    new_dict[obj.__class__.__name__ + "." + obj.id] = obj

        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj) if self.__session else None

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit() if self.__session else None

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        self.__session.delete(obj) if self.__session and obj else None

    def reload(self):
        """reloads data from the database"""
        from sqlalchemy.orm import scoped_session, sessionmaker

        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, id):
        """Retrieve an object based on class and ID"""
        if not cls or not id:
            return
        for clss in classes:
            if cls == clss or cls is classes[clss]:
                if self.__session:
                    return (
                        self.__session.query(classes[clss])
                        .filter_by(id=id)
                        .first()
                    )

    def count(self, cls=None):
        """
        Count the number of objects in storage matching the given class
        if cls is None, return the count of all objects in storage
        if cls = "all", will default to None to return the count of all objects
        """
        cls = None if cls == "all" else cls
        return len(self.all(cls))

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove() if self.__session else None
