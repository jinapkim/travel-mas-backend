from __future__ import annotations
from typing import List, Dict, Any
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.mutable import MutableList
from db import db
from libs.stopwords import removeStopwords


class ExperienceModel(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    geo_location = db.Column(db.String())
    image_url = db.Column(db.String())
    rating = db.Column(db.Integer, nullable=False)
    keywords = db.Column(MutableList.as_mutable(postgresql.ARRAY(db.String())))

    #trip = db.relationship("TripExperienceModel", backref="experience", lazy="dynamic")
    #ratings = db.relationship("RatingModel", backref="rating", lazy="dynamic")

    @classmethod
    def find_by_id(cls, _id: int) -> ExperienceModel:
        return cls.query.get(_id)

    @classmethod
    def find_all(cls) -> List[ExperienceModel]:
        return cls.query.all()

    @classmethod
    def find_by_keyword(cls, keyword: str) -> List[ExperienceModel]:
        return cls.query.filter(cls.keywords.contains([keyword.lower()])).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def populate_keywords(self):
        self.keywords = []
        # add title to keywords
        self.keywords.append(self.title.lower())
        # add complete address to keywords
        self.keywords.append(self.location.lower())
        # add address, city, and state to array of keywords
        address = self.location.split(", ")
        for item in address:
            if item.lower() not in self.keywords:
                self.keywords.append(item.lower())
        # extract words from description to add to array of keywords
        description_kws = removeStopwords(self.description)
        for word in description_kws:
            if word.lower() not in self.keywords:
                self.keywords.append(word.lower())

    def update_entry(self) -> None:
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "geo_location": self.geo_location,
            "image_url": self.image_url,
            "rating": self.rating,
            "keywords": self.keywords
        }
