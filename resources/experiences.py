from flask_restful import Resource


class Experiences(Resource):
    @classmethod
    def get(cls):
        ...

    @classmethod
    def post(cls):
        ...


class Experience(Resource):
    @classmethod
    def get(cls, experience_id: int):
        ...

    @classmethod
    def put(cls, experience_id: int):
        ...

    @classmethod
    def delete(cls, experience_id: int):
        ...
