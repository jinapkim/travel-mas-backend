from __future__ import annotations
import bcrypt

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
        return cls.query.filter_by(user_name=user_name.lower()).first()

    @classmethod
    def find_by_id(cls, _id: int) -> UserModel:
        return cls.query.filter_by(id=_id).first()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def save_to_db(self) -> None:
        # Hash password and set password to hashed value.
        self.password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.user_name = self.user_name.lower()

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
