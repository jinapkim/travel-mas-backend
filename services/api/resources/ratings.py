from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from models.rating import RatingModel
from db import db, Database

class Ratings(Resource):

    @classmethod
    def get(cls):
        ratings = RatingModel.query.all()
        results = {'ratings': [rating.to_dict() for rating in ratings]}

        return results, 200

    @classmethod
    @jwt_required()
    def post(cls): 
        data = request.get_json()
        new_rating = RatingModel(
            user_id = current_user.id,
            experience_id = data['experience_id'],
            thumbs_up = data['thumbs_up']
        )
        Database.add(new_rating)

        return new_rating.to_dict(), 201


class Rating(Resource):

    @classmethod
    def get(cls, rating_id):
        rating = RatingModel.query.get(rating_id)
        if not rating:
            return {'Error': 'Rating not found'}, 404

        return rating.to_dict(), 200

    @classmethod
    @jwt_required()
    def put(cls, rating_id):
        rating = RatingModel.query.get(rating_id)
        if not rating:
            return {'Error': 'Rating not found'}, 404

        if rating.user_id != current_user.id:
            return {"Error": "Forbidden. User does not have sufficient permissions."}, 403

        data = request.get_json()
        rating.user_id = current_user.id
        rating.experience_id = data['experience_id']
        rating.thumbs_up = data['thumbs_up']

        Database.commit()

        return rating.to_dict(), 200

    @classmethod
    @jwt_required()
    def delete(cls, rating_id):
        rating = RatingModel.query.get(rating_id)
        if not rating:
            return {'Error': 'Rating not found'}, 404

        if rating.user_id != current_user.id:
            return {"Error": "Forbidden. User does not have sufficient permissions."}, 403

        Database.delete(rating)

        return {'Message': 'Rating deleted'}, 200


class RatingsExperience(Resource):
    @classmethod
    def get(cls, experience_id):
        ratings = (
            RatingModel
            .query
            .filter(RatingModel.experience_id==experience_id)
            .all()
        )

        return {
            "count": len(ratings),
            "ratings": [rating.to_dict() for rating in ratings],
            "postive_ratings_count": len([rating for rating in ratings if rating.thumbs_up == True]),
            "negative_ratings_count": len([rating for rating in ratings if rating.thumbs_up == False])
        }, 200

    @classmethod
    @jwt_required()
    def delete(cls, experience_id):
        rating = (
            RatingModel
            .query
            .filter(
                RatingModel.experience_id==experience_id,
                RatingModel.user_id==current_user.id
            )
            .first()
        )
        if not rating:
            return {"Error": "Rating Not Found."}, 404
        Database.delete(rating)

        return {"Message": "Rating Sucessfully Deleted."}, 200
