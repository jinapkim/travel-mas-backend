from flask import request
from flask_restful import Resource
from models.trip import TripModel
from models.experience import ExperienceModel
from db import Database

class Trips(Resource):

    @classmethod
    def get(cls):
        # Check for user_id in query string and get trips by user
        user_id = request.args.get("user_id", -1)
        if user_id == "null":
            return {"trips": [{"id": 0, "name": "No Trips Found"}]}
        if user_id.isnumeric:
            trips = TripModel.query.filter(TripModel.user_id==int(user_id)).all()
            return {"trips": [trip.to_dict() for trip in trips]}

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


class TripExperience(Resource):

    @classmethod
    def post(cls, trip_id, experience_id):
        trip = TripModel.query.get(trip_id)
        if not trip: 
            return {'Error': 'Trip not found'}, 404
        
        experience = ExperienceModel.query.get(experience_id)
        if not experience: 
            return {'Error': 'Experience not found'}, 404

        new_entry = trip.experiences.append(experience)
        Database.commit()

        return {'Message': 'Trip-experience added'}, 200

    @classmethod
    def delete(cls, trip_id, experience_id):
        trip = TripModel.query.get(trip_id)
        experience = ExperienceModel.query.get(experience_id)
        if not trip:
            return {"Error": "Trip not found"}, 404
        if not experience:
            return {"Error": "Experience not found"}, 404

        trip.experiences.remove(experience)
        Database.commit()

        return {"Message": f"Epxerience {experience_id} Removed From Trip ID {trip_id}"}

    @classmethod
    # Get all experiences tied to a specific trip 
    def get(cls, trip_id):
        trip = TripModel.query.get(trip_id)
        if not trip: 
            return {'Error': 'Trip not found'}, 404

        experiences = trip.experiences.all()
        return {'experiences': [experience.to_dict() for experience in experiences]}, 200
