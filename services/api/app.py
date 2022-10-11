import os

from flask import Flask
from flask_restful import Api

from resources.hello_world import HelloWorld
from resources.users import UserRegister, User
from models.user import UserModel
from db import db


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///" + app.root_path + "../../data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()

    # TODO: Remove this line. Only for testing purposes
    UserModel(first_name="adam", last_name="bratcher", user_name="abratcher", password="password123").save_to_db()

api.add_resource(HelloWorld, "/") # TODO: Remove this line also
api.add_resource(User, "/user/<string:user_name>")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    app.run(debug=True)
