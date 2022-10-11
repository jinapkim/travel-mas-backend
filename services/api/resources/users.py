from flask import request
from flask_restful import Resource

from models.user import UserModel
from libs.password import Password


class UserRegister(Resource):
    """Resource to register a new user."""
    @classmethod
    def post(cls):
        user_json = request.get_json()
        # TODO: add json validation. Marshmallow Library?
        if UserModel.find_by_username(user_json["user_name"]):
            return {"message": "Invalid Username. Username already taken."}, 400

        # Hash password and set password to hashed value.
        pword = Password()
        pword.password = user_json["password"]
        user_json["password"] = pword.password

        UserModel(**user_json).save_to_db()


class User(Resource):
    @classmethod
    def get(cls, user_name: str):
        user = UserModel.find_by_username(user_name)
        if not user:
            return {"message": "User Not Found."}, 404
        return user.to_json, 200
