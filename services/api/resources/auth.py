from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    set_access_cookies)


class AuthRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        resp = jsonify({"access_token": access_token})
        set_access_cookies(resp, access_token)
        return resp
