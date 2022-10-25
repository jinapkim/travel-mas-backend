from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from models.experience import ExperienceModel
from models.image import ImageModel
from schemas.experience import ExperienceSchema
from libs.location import FindLatLong

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
