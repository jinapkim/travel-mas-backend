import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.users import User, UserList, UserRegister, UserLogin
from db import db


app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///" + app.root_path + "../../data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "MySuperSecretKey" # This should be moved elsewhere at some point
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

api.add_resource(User, "/user/<string:user_name>")
api.add_resource(UserList, "/users")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")


if __name__ == "__main__":
    app.run(debug=True)
