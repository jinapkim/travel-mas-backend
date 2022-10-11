from __future__ import annotations
from typing import Dict

from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    user_name = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    # trips = db.relationship("TripModel", backref="user", lazy="dynamic")
    # experiences = db.relationship("ExperienceModel", backref="experience", lazy="dynamic")
    # ratings = db.relationship("RatingModel", backref="rating", lazy="dynamic")

    @classmethod
    def find_by_username(cls, user_name: str) -> UserModel:
        return cls.query.filter_by(user_name=user_name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> UserModel:
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name
        }
