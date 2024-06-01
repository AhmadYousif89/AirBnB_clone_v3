#!/usr/bin/python
"""Module for Amenity class"""
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from models import storage_type


class Amenity(BaseModel, Base):
    """Representation of Amenity"""

    if storage_type == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""
