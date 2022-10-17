from __future__ import annotations
from typing import List, Dict, Any
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.mutable import MutableList
from db import db


class ExperienceModel(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    geo_location = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    keywords = db.Column(MutableList.as_mutable(postgresql.ARRAY(db.String())), nullable=False)

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

    def update_keywords(self, keywords):
        keywords = [str(kw.lower()) for kw in keywords]
        keyword_set = set(self.keywords)

        for kw in keywords:
            if kw not in keyword_set:
                self.keywords.append(kw)

    def update_entry(self) -> None:
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "geo_location": self.geo_location,
            "image": self.image,
            "rating": self.rating,
            "keywords": self.keywords
        }
