#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel
from models.city import City


class State(BaseModel, Base):
    """ State class """

    if models.storage_type == "db":
        __tablename__ = "states"

        name = Column(String(128), nullable=False)

        # cities = relationship("City", back_populates="state",
        #                       cascade="all, delete, delete-orphan")
        # DBStorage - what works;
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")

    else:
        name = ""


    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_type != "db":

        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            cities = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    cities.append(city)
            return cities
