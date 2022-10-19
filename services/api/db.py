from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Database():

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def add(cls, resource): 
        db.session.add(resource)
        db.session.commit()

    @classmethod
    def delete(cls, resource):
        db.session.delete(resource)
        db.session.commit()
