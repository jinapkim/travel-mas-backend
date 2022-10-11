from flask_restful import Resource


class HelloWorld(Resource):
    def get(cls):
        return {"hello": "world"}
