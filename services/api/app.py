import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from marshmallow import ValidationError

from models.user import UserModel
from resources.experiences import Experience, Experiences, UserExperiences, ExperienceRating
from resources.users import User, UserList, UserRegister, UserLogin, UserLogout
from resources.trips import Trip, Trips, TripExperience
from resources.ratings import Ratings, Rating
from resources.images import Images, Image

from db import db
from ma import ma


app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
CORS(app, resources={r"*": {"origins": "*"}})

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5432/travel_mas")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["JWT_SECRET_KEY"] = "MySuperSecretKey" # This should be moved elsewhere at some point


db.init_app(app)
ma.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()


@app.errorhandler(ValidationError)
def marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.find_by_id(identity)


# User Endpoints
api.add_resource(User, "/users/<string:user_name>")
api.add_resource(UserList, "/users")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")

# Experience Endpoints
api.add_resource(Experience, "/experiences/<int:experience_id>")
api.add_resource(Experiences, "/experiences")
api.add_resource(UserExperiences, "/users/<int:user_id>/experiences")

# Trip Endpoints
api.add_resource(Trips, '/trips')
api.add_resource(Trip, '/trips/<int:trip_id>')

# Trip-experience Endpoints
api.add_resource(TripExperience, '/trips/<int:trip_id>/experiences', '/trips/<int:trip_id>/experiences/<int:experience_id>')

# Rating Endpoints
api.add_resource(Ratings, '/ratings')
api.add_resource(Rating, '/ratings/<int:rating_id>')

# Experience-rating endpoints
api.add_resource(ExperienceRating, '/experiences/<int:experience_id>/ratings')

# Images Endpoint
api.add_resource(Images, "/images")
api.add_resource(Image, "/images/<int:image_id>")

if __name__ == "__main__":
    app.run(debug=True)
