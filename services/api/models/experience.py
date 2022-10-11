from sqlalchemy.dialects.postgresql import ARRAY

from typing import Dict, Any
from db import db


class ExperienceModel(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    geo_location = db.Column(db.String())
    image = db.Column(db.String())
    rating = db.Column(db.Integer)
    keywords = db.Column(ARRAY)

    trip = db.relationship("TripExperienceModel", backref="experience", lazy="dynamic")
    ratings = db.relationship("RatingModel", backref="rating", lazy="dynamic")

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "geo_location": self.geo_location,
            "image": self.image,
            "rating": self.rating,
            "keywords": self.keywords
        }
