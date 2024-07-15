#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String

import models
from models.base_model import Base, BaseModel


class Amenity(BaseModel, Base):
    if models.storage_type == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
