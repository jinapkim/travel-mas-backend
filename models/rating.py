from db import db


class RatingModel(db.Model):
    __tablename__ = "ratings"

    user_id = db.Column(db.Interger, db.ForeignKey("users.id"), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey("experiences.id"), nullable=False)
    thumbs_up = db.Column(db.Boolean, nullable=False)

    def __init__(self, user_id: int, experience_id: int, thumbs_up: bool):
        self.user_id = user_id
        self.experience_id = experience_id
        self.thumbs_up = thumbs_up
