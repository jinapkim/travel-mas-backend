from db import db

class RatingModel(db.Model):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey("experiences.id"), nullable=False)
    thumbs_up = db.Column(db.Boolean, nullable=False)

    def to_dict(self): 
        return {
            'id': self.id,
            'user_id': self.user_id, 
            'experience_id': self.experience_id,
            'thumbs_up': self.thumbs_up
        }

    # def __init__(self, user_id, experience_id, thumbs_up):
    #     self.user_id = user_id
    #     self.experience_id = experience_id
    #     self.thumbs_up = thumbs_up
