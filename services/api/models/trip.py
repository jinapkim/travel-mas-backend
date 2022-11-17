from db import db


trip_experience = db.Table('trip_experience',
    db.Column('trip_id', db.Integer, db.ForeignKey("trips.id"), nullable=False, primary_key=True),
    db.Column('experience_id', db.Integer, db.ForeignKey("experiences.id"), nullable=False, primary_key=True),
)

class TripModel(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(), nullable=False)
    experiences = db.relationship('ExperienceModel', secondary=trip_experience, lazy='dynamic', backref='trips')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name
        }
        
