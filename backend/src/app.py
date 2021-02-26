import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .models import db_drop_and_create_all, setup_db, Movies, Actors
from .auth import AuthError, requires_auth


# create and configure the app
app = Flask(__name__)
CORS(app)
setup_db(app)

# CORS Headers
@app.after_request
def after_request(response):

    # Allow requests headers ( Content-Type, Authorization)
    response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')

    # Allow specific requests methods (GET, POST, PATCH, DELETE, OPTIONS)
    response.headers.add('Access-Control-Allow-Methods',
                            'GET,PATCH,POST,DELETE,OPTIONS')
    return response
    
#Run ONLY first time you start the app
# db_drop_and_create_all()

## ROUTES
# Check the index route is running smoothly
@app.route('/')
def index():
    return "Healthy"

'''
    GET /movies
    - Retrieves movies stored in db
    - Request arguments: n/a
    - Returns: A list of movies ordered by id and containing the title, and release year
'''

@app.route('/movies')
@requires_auth('get:movies')
def get_movies(payload):
    try:
        # query movies from db
        movies = Movies.query.order_by(Movies.id).all()

        return jsonify({
            'success': True,
            # return list of movies from db
            'movies': [movie.style() for movie in movies]
        }), 200

    except:
        abort(422)

'''
    GET /actors
    - Retrieves actors stored in db
    - Request arguments: n/a
    - Returns: A list of actors ordered by id and containing the name, age, and gender
'''

@app.route('/actors')
@requires_auth('get:actors')
def get_actors(payload):

    try:
        # Query all actors from the database
        actors = Actors.query.order_by(Actors.id).all()

        return jsonify({
            'success': True,
            'actors': [actor.style() for actor in actors]
        }), 200

    except:
        abort(422)

'''
    POST /movies
    - Adds new movie instance in db
    - Request arguments: n/a
    - Returns: The newly added movie containing id, the title, and release year
'''

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movies(payload):
    #load data 
    data = request.get_json()

    if not ('title' in data and 'release_date' in data):
        abort(422)

    title = data.get('title')
    release_date = data.get('release_date')

    try:
        movie = Movies(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': [movie.style()],
        }), 200

    except:
        abort(422)

'''
    POST /actors
    - Adds new actor instance in db
    - Request arguments: n/a
    - Returns: The newly added actor containing id, the name, age, and gender
'''

@app.route('/actors',  methods=['POST'])
@requires_auth('post:actors')
def post_actors(payload):
    #load data 
    data = request.get_json()

    if not ('name' in data and 'age' in data and 'gender' in data):
        abort(422)

    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')

    try:
        actor = Actors(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': [actor.style()],
        })

    except:
        abort(422)

'''
    PATCH /movies/<int:id>
    - Updates a movie instance in db
    - Request arguments: id
    - Returns: The newly added movie containing id, the title, and release year
'''

@app.route('/movies/<id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movies(payload, id):
    movie = Movies.query.get(id)

    if not movie:
        abort(404)
    else:
        try:

            data = request.get_json()

            title = data.get('title')
            release_date = data.get('release_date')

            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date

            movie.update()

            return jsonify({
                'success': True,
                'movies': [movie.style()]
            })
        except:
            abort(422)

'''
    PATCH /actors/<int:id>
    - Updates an actor instance in db
    - Request arguments: id
    - Returns: The newly added actor containing id, the title, and release year
'''

@app.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actors(payload, id):
    actor = Actors.query.get(id)

    if not actor:
        abort(404)
    else:
        try:

            data = request.get_json()

            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')

            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender

            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.style()]
            })
        except:
            abort(422)


'''
    DELETE /movies/<int:id>
    - Deletes a movie instance in db
    - Request arguments: id
    - Returns: the id of deleted movie
'''

@app.route("/movies/<id>", methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(payload, id):

    movie = Movies.query.get(id)

    if not movie:
        abort(404)
    else:
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)

'''
    DELETE /actors/<int:id>
    - Updates an actor instance in db
    - Request arguments: id
    - Returns: the id of deleted actor
'''

@app.route("/actors/<id>", methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(payload, id):

    actor = Actors.query.get(id)

    if not actor:
        abort(404)
    else:
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)

## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify({
        "success": False,
        "error": ex.status_code,
        'message': ex.error
    }), 401