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
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Movies(db.Model):    
    __tablename__ = "movies"

    # movie db columns
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(180), unique=True, nullable=False)
    release_date = Column(String(180), nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f"( Movie {self.id} {self.title} {self.release_date} )"

    # a method to format movie db
    def style(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    # insert (post) instance into db
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # delete instance in db
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # update (patch) instance in db
    def update(self):
        db.session.commit()

'''
Actors
a persistent actor entity, extends the base SQLAlchemy Model
'''

class Actors(db.Model):
    __tablename__ = "actors"

    # actors db columns
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

    # a method to format actors db
    def style(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    # insert (post) actor into db 
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # delete instance from db
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # update (patch) actor in db
    def update(self):
        db.session.commit()
