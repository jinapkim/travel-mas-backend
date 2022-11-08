from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from models.experience import ExperienceModel
from models.image import ImageModel
from models.rating import RatingModel
from schemas.experience import ExperienceSchema
from libs.location import FindLatLong
from db import db, Database

SCHEMA = ExperienceSchema()


class Experiences(Resource):
    @classmethod
    def get(cls):
        keyword = request.args.get("keyword")
        if keyword is not None:
            experiences = ExperienceModel.find_by_keyword(keyword)
        else:
            experiences = ExperienceModel.find_all()

        return {
            "count": len(experiences),
            "experiences": [experience.to_dict() for experience in experiences]
        }, 200

    @classmethod
    @jwt_required()
    def post(cls):
        experience_json = request.get_json()

        experience = SCHEMA.load(experience_json)
        # popultate keywords from title, location, and description
        experience.populate_keywords()
        # add lat, long
        experience.geo_location = FindLatLong(experience.location)
        experience.user_id = current_user.id

        image = ImageModel.find_by_id(experience.image_id)
        if image:
            experience.image_url = image.url
        experience.save_to_db()

        return experience.to_dict(), 201


class Experience(Resource):
    @classmethod
    def get(cls, experience_id: int):
        experience = ExperienceModel.find_by_id(experience_id)
        if not experience:
            return {"message": "Experience Not Found"}, 404
        return experience.to_dict(), 200

    @classmethod
    @jwt_required()
    def put(cls, experience_id: int):
        edited_experience = request.get_json()
        experience = ExperienceModel.find_by_id(experience_id)

        if not experience:
            return {"message": "Experience Not Found"}, 404

        if current_user.id != experience.user_id:
            return {"message": f"Forbidden. User Is Not Owner Of {experience.title} Experience."}, 403

        for key in edited_experience:
            if key == "title":
                setattr(experience, key, edited_experience[key])
            elif key == "location":
                setattr(experience, key, edited_experience[key])  
                setattr(experience, "geo_location", FindLatLong(edited_experience[key]))
            elif key == "description":
                setattr(experience, key, edited_experience[key])
            else:
                setattr(experience, key, edited_experience[key])

        experience.populate_keywords()        

        experience.update_entry()

        return experience.to_dict(), 200

    @classmethod
    @jwt_required()
    def delete(cls, experience_id: int):
        experience = ExperienceModel.find_by_id(experience_id)
        if not experience:
            return {"message": "Experience Not Found"}, 404

        if current_user.id != experience.user_id:
            return {"message": f"User Is Not Owner Of {experience.title} Experience."}, 403

        experience.delete_from_db()
        return {"message": "Experience successfully deleted"}, 200


class UserExperiences(Resource):
    @classmethod
    def get(cls, user_id: str):
        experiences = ExperienceModel.query.filter(ExperienceModel.user_id==user_id).all()
        return {
            "count": len(experiences),
            "experiences": [experience.to_dict() for experience in experiences]
        }, 200

class ExperienceRating(Resource): 
    @classmethod
    def get(cls, experience_id: int):
        experience = ExperienceModel.query.get(experience_id)
        if not experience:
            return {'Error': 'Experience not found'}, 404

        ratings = experience.ratings.all()
        result = 0
        for rating in ratings:
            print(rating.thumbs_up)
            if rating.thumbs_up == True: 
                result = result + 1
            else:
                result = result - 1
        
        return {'Rating': result}, 200

    @classmethod
    def post(cls, experience_id:int):
        data = request.get_json()

        experience = ExperienceModel.query.get(experience_id)
        if not experience: 
            return {'Error': 'Experience not found'}, 404

        # Check if user has already rated this experience
        user = data['user_id']
        results = experience.ratings.filter_by(user_id=user).count()
        if results > 0:
            return {'Error': 'User has already rated this experience'}, 400

        # Create new Rating 
        new_rating = RatingModel(
            user_id = data['user_id'],
            experience_id = experience_id,
            thumbs_up = data['thumbs_up']
        )
        Database.add(new_rating)

        # Add Rating to Experience
        experience.ratings.append(new_rating)
        Database.commit()
        print(experience.ratings)

        return {'Message': 'Rating added to experience'}, 200
