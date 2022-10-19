from flask import request
from flask_restful import Resource
from models.rating import RatingModel
from db import db, Database

class Ratings(Resource):

    @classmethod
    def get(cls):
        ratings = RatingModel.query.all()
        results = {'ratings': [rating.to_dict() for rating in ratings]}

        return results, 200

    @classmethod
    def post(cls): 
        data = request.get_json()
        new_rating = RatingModel(
            user_id = data['user_id'],
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
    def put(cls, rating_id):
        rating = RatingModel.query.get(rating_id)
        if not rating:
            return {'Error': 'Rating not found'}, 404

        data = request.get_json()
        rating.user_id = data['user_id']
        rating.experience_id = data['experience_id']
        rating.thumbs_up = data['thumbs_up']

        Database.commit()

        return rating.to_dict(), 200

    @classmethod
    def delete(cls, rating_id):
        rating = RatingModel.query.get(rating_id)
        if not rating:
            return {'Error': 'Rating not found'}, 404

        Database.delete(rating)

        return {'Message': 'Rating deleted'}, 200
