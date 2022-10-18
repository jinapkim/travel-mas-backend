from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from models.experience import ExperienceModel
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
            "experiences": [experience.to_json() for experience in experiences]
        }, 200

    @classmethod
    @jwt_required()
    def post(cls):
        experience_json = request.get_json()
        experience = SCHEMA.load(experience_json)

        # update to lat, long
        experience.geo_location = FindLatLong(experience.geo_location)
        # save all keywords as lower case
        experience.keywords = [keyword.lower() for keyword in experience.keywords]
        experience.user_id = current_user.id

        experience.save_to_db()

        return experience.to_json(), 201


class Experience(Resource):
    @classmethod
    def get(cls, experience_id: int):
        experience = ExperienceModel.find_by_id(experience_id)
        if not experience:
            return {"message": "Experience Not Found"}, 404
        return experience.to_json(), 200

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
            if key == "geo_location":
                setattr(experience, key, FindLatLong(edited_experience[key]))
            elif key == "keywords":
                experience.update_keywords(edited_experience[key])
            else:
                setattr(experience, key, edited_experience[key])

        experience.update_entry()

        return experience.to_json(), 200

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
