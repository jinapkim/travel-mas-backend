import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from resources.users import User, UserList, UserRegister, UserLogin
from resources.experiences import Experience, Experiences
from models.user import UserModel
from db import db
from ma import ma


app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///" + app.root_path + "../../data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "MySuperSecretKey" # This should be moved elsewhere at some point

db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

@app.errorhandler(ValidationError)
def marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(User, "/user/<string:user_name>")
api.add_resource(UserList, "/users")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(Experience, "/experience/<int:experience_id>")
api.add_resource(Experiences, "/experiences")

if __name__ == "__main__":
    app.run(debug=True)
