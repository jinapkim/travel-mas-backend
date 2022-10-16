from __future__ import annotations
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
    keywords = db.Column(db.String())

    #trip = db.relationship("TripExperienceModel", backref="experience", lazy="dynamic")
    #ratings = db.relationship("RatingModel", backref="rating", lazy="dynamic")

    @classmethod
    def find_by_id(cls, _id: int) -> ExperienceModel:
        return cls.query.get(_id)

    @classmethod
    def find_all(cls) -> ExperienceModel:
        all_experiences = cls.query.all()
        results = [
            {
                "id": experience.id,
                "title": experience.title,
                "description": experience.description,
                "geo_location": experience.geo_location,
                "image": experience.image,
                "rating": experience.rating,
                "keywords": experience.keywords
            } for experience in all_experiences]   

        return {"count": len(results), "experiences": results}

    @classmethod
    def find_by_keyword(cls, exp_keyword: str) -> ExperienceModel:
        all_experiences = cls.query.all()
        results = []
        for experience in all_experiences:
            if exp_keyword in experience.keywords:
                results.append(experience.to_json()) 
        
        return results

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

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
