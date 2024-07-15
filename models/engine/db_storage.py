#!/usr/bin/python3

import os
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from sqlalchemy import create_engine
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}



class DBStorage:
    """
    This class represents the database storage for the AirBnB clone project.
    It is responsible for managing the connection to the database and providing
    methods to interact with the data.

    Attributes:
        __engine (sqlalchemy.engine.Engine): The database engine object.
        __session (sqlalchemy.orm.Session): The database session object.

    Methods:
        __init__: Initializes the DBStorage object.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        This method is responsible for initializing the database connection.
        """

        HBNB_MYSQL_USER = os.environ.get("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = os.environ.get("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = os.environ.get("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = os.environ.get("HBNB_MYSQL_DB")
        HBNB_ENV = os.environ.get("HBNB_ENV")

        self.__engine = create_engine(
            f'mysql+mysqldb://{HBNB_MYSQL_USER}:\
{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}',
            pool_pre_ping=True
        )
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the current database session"""


        objects = {}
        if cls is None:
            for cls in classes:
                cls_name = classes[cls].__name__
                objs = self.__session.query(classes[cls]).all()
                for obj in objs:
                    key = "{}.{}".format(cls_name, obj.id)
                    objects[key] = obj
        else:
            if type(cls) == str and cls in classes:
                cls = classes[cls]
            cls_name = cls.__name__
            if cls_name in classes:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = "{}.{}".format(cls_name, obj.id)
                    objects[key] = obj

        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create the current database session"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute"""
        if self.__session:
            self.__session.close()
