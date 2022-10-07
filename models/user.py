from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    user_name = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    trips = db.relationship("TripModel", backref="user", lazy="dynamic")
    experiences = db.relationship("ExperienceModel", backref="experience", lazy="dynamic")
    ratings = db.relationship("RatingModel", backref="rating", lazy="dynamic")


    def __init__(self, id: int, first_name: str, last_name: str, user_name: str, password: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = db.Column(db.String())
