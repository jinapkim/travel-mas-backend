from db import db

class TripModel(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(), nullable=False)

    # trips = db.relationship("TripExperienceModel", backref="trip", lazy="True")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name
        }
        


# class TripExperienceModel(db.Model):
#     __tablename__ = "trip_experience"
# 
#     trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)
#     experience_id = db.Column(db.Integer, db.ForeignKey("experiences.id"), nullable=False)
# 
#     def __init__(self, trip_id: int, experience_id: int):
#         self.trip_id = trip_id
#         self.experience_id = experience_id
