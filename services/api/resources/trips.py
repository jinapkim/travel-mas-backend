from flask import request
from flask_restful import Resource
from models.trip import TripModel
from db import db, Database

class Trips(Resource):

    @classmethod
    def get(cls):
        trips = TripModel.query.all()
        results = {'trips': [trip.to_dict() for trip in trips]}

        return results, 200
        
    @classmethod
    def post(cls):
        data = request.get_json()
        new_trip = TripModel(
            user_id = data['user_id'],
            name = data['name']
        )
        Database.add(new_trip)

        return new_trip.to_dict(), 201

class Trip(Resource):

    @classmethod
    def get(cls, trip_id):
        trip = TripModel.query.get(trip_id)
        if not trip: 
            return {'Error': 'Trip not found'}, 404

        return trip.to_dict(), 200
        
    @classmethod
    def delete(cls, trip_id):
        trip = TripModel.query.get(trip_id)
        if not trip: 
            return {'Error': 'Trip not found'}, 404

        Database.delete(trip)
        
        return {'Message': 'Trip deleted'}, 200

    @classmethod
    def put(cls, trip_id):
        trip = TripModel.query.get(trip_id)
        if not trip: 
            return {'Error': 'Trip not found'}, 404

        data = request.get_json()
        trip.user_id = data['user_id']
        trip.name = data['name']

        Database.commit()

        return trip.to_dict(), 200


# class TripExperience(Resource):
# 
#     @classmethod
#     def post(cls):
#         pass
