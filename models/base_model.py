#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

# from sqlalchemy.orm import sessionmaker

# Create a base class for declarative models
if models.storage_type  == "db":
    Base = declarative_base()
else:
    Base = object
time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """A base class for all hbnb models"""

    if models.storage_type == 'db':
        id = Column(String(60), primary_key=True, nullable=False, unique=True)
        created_at = Column(DateTime, default=datetime.now(timezone.utc),
                            nullable=False)
        updated_at = Column(DateTime, default=datetime.now(timezone.utc),
                            nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            # for key, value in kwargs.items():
                # if key != "__class__":
                #     setattr(self, key, value)
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
            if kwargs.get("updated_at", None):
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("created_at", None):
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if '__class__' in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)
