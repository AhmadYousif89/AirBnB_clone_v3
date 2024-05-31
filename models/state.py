#!/usr/bin/python3
"""Module for State class"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage_type


class State(BaseModel, Base):
    """Representation of state"""

    if storage_type == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        name = ""

        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            from models.city import City
            from models import storage

            return [
                city
                for city in storage.all(City).values()
                if city.state_id == self.id
            ]
