#!/usr/bin/python
"""Module for Place class"""
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from models.base_model import BaseModel, Base
from models import storage_type

if storage_type == 'db':
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id', onupdate='CASCADE', ondelete='CASCADE'),
            primary_key=True,
        ),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id', onupdate='CASCADE', ondelete='CASCADE'),
            primary_key=True,
        ),
    )


class Place(BaseModel, Base):
    """Representation of Place"""

    if storage_type == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship(
            "Review", backref="place", cascade="all, delete"
        )
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            backref="place_amenities",
            viewonly=False,
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review
            from models import storage

            return [
                review
                for review in storage.all(Review).values()
                if review.place_id == self.id
            ]

        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity
            from models import storage

            return [
                amenity
                for amenity in storage.all(Amenity).values()
                if amenity.place_id == self.id
            ]

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)
