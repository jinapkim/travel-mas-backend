from flask_restful import Resource


class Ratings(Resource):
    @classmethod
    def get(cls, experience_id):
        ...

    @classmethod
    def post(cls, experience_id):
        ...

    @classmethod
    def put(cls, experience_id):
        ...

    @classmethod
    def delete(cls, experience_id):
        ...
