from flask import Flask
from flask_restful import Api

from resources.experiences import Experience, Experiences


app = Flask(__name__)
api = Api(app)

api.add_resource(Experiences, "/experiences")
api.add_resource(Experience, "/expereince/<int:experience_id>")


if __name__ == "__main__":
    app.run()
