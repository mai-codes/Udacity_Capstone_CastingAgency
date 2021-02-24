import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

database_filename = "agency.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Movies
a persistent drink entity, extends the base SQLAlchemy Model
'''
class Movies(db.Model):    
    __tablename__ = "movies"

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(180), unique=True, nullable=False)
    release_date = Column(String(180), nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f"( Movie {self.id} {self.title} {self.release_date} )"

    def style(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Actors(db.Model):
    __tablename__ = "actors"

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True, nullable=False)
    name = Column(String(180), unique=True, nullable=False)
    age =  Column(Integer().with_variant(Integer, "sqlite"), nullable=False)
    gender = Column(String(180), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f"( Actor {self.id} {self.name} {self.age} {self.gender} )"

    def style(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
