from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from models.user import UserModel
from schemas.user import UserSchema


class UserRegister(Resource):
    """Resource to register a new user."""
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = UserSchema().load(user_json)

        if UserModel.find_by_username(user.user_name):
            return {"message": "Invalid Username. Username already taken."}, 400

        user.save_to_db()
        return {"id": user.id, "user_name": user.user_name}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_name = request.json.get("user_name", None)
        password = request.json.get("password", None)

        if user_name is not None:
            user = UserModel.find_by_username(user_name)
            if not user:
                return {"message": "User Not Found."}, 404

            if not user.check_password(password):
                return {"message": "Ivalid Password."}, 401
            else:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
            }, 201


class User(Resource):
    @classmethod
    def get(cls, user_name: str):
        user = UserModel.find_by_username(user_name)
        if not user:
            return {"message": "User Not Found."}, 404
        return UserSchema().dump(user), 200


class UserList(Resource):
    @classmethod
    def get(cls):
        users = UserModel.query.all()
        return {"users": [{"id": user.id, "user_name": user.user_name} for user in users]}, 200
