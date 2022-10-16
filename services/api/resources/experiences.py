from hashlib import new
from flask import request
from flask_restful import Resource

from models.experience import ExperienceModel
from libs.location import FindLatLong


class Experiences(Resource):
    @classmethod
    def get(cls):
        keyword = request.args.get("keyword")
        if keyword:
            experiences = ExperienceModel.find_by_keyword(keyword)
            if not experiences:
                return {"message": "Sorry. No experiences match that keyword"}, 404
            return experiences
        else:
            experiences = ExperienceModel.find_all()
            return experiences

    @classmethod
    def post(cls):
        experience_json = request.get_json()
        location = FindLatLong(experience_json["geo_location"])

        ExperienceModel(
            title = experience_json["title"],
            description = experience_json["description"],
            geo_location = location,
            image = experience_json["image"],
            rating = experience_json["rating"],
            keywords = experience_json["keywords"]
            ).save_to_db()
        
        return {"message": "Experience successfully created"}, 201


class Experience(Resource):
    @classmethod
    def get(cls, experience_id: int):
        experience = ExperienceModel.find_by_id(experience_id)
        if not experience:
            return {"message": "Experience Not Found"}, 404
        return experience.to_json(), 200

    @classmethod
    def put(cls, experience_id: int):
        edited_experience = request.get_json()
        experience = ExperienceModel.find_by_id(experience_id)
        if not experience:
            return {"message": "Experience Not Found"}, 404

        if "title" in edited_experience:
            experience.title = edited_experience["title"]
        if "description" in edited_experience:
            experience.description = edited_experience["description"]
        if "geo_location" in edited_experience:
            location = FindLatLong(edited_experience["geo_location"])
            experience.geo_location = location
        if "image" in edited_experience:
            experience.image = edited_experience["image"]
        if "rating" in edited_experience:
            experience.rating = edited_experience["rating"]
        if "keywords" in edited_experience:
            experience.keywords = edited_experience["keywords"]

        experience.save_to_db()
        return {"message": "Experience successfully updated"}, 200

    @classmethod
    def delete(cls, experience_id: int):
        experience = ExperienceModel.find_by_id(experience_id)
        if not experience:
            return {"message": "Experience Not Found"}, 404
        experience.delete_from_db()
        return {"message": "Experience successfully deleted"}, 200
