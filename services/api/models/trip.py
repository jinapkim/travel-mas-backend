from db import db
from models.user import UserModel

class TripModel(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(), nullable=False)

    trips = db.relationship("TripExperienceModel", backref="trip", lazy="dynamic")


class TripExperienceModel(db.Model):
    __tablename__ = "trip_experience"

    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"))
    experience_id = db.Column(db.Integer, db.ForeignKey("experiences.id"))

    def __init__(self, trip_id: int, experience_id: int):
        self.trip_id = trip_id
        self.experience_id = experience_id
