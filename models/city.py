#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel


class City(BaseModel, Base):
    """ The city class, contains state ID and name """

    if models.storage_type == "db":
        __tablename__ = "cities"

        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)

    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
