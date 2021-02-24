import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .models import db_drop_and_create_all, setup_db, Movies, Actors
# from db import setup_db
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
# Simple health check
@app.route('/')
def index():
    return "Healthy"

'''
    GET /movies
    - Retrieves movies stored in db
    - Request arguments: None
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
    - Retrieves movies stored in db
    - Request arguments: None
    - Returns: A list of movies ordered by id and containing the title, and release year
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



@app.route('/movies',  methods=['POST'])
@requires_auth('post:movies')
def post_movies(jwt):
    #load data 
    data = request.get_json()

    if not ('title' in data and 'recipe' in data):
        abort(422)

    title = data.get('title')
    recipe = data.get('recipe')

    try:
        newdrink = Drink(title=title, recipe=json.dumps(recipe))
        newdrink.insert()

        return jsonify({
            'success': True,
            'drinks': [newdrink.long()],
        })

    except:
        abort(422)


# @app.route('/drinks/<id>', methods=['PATCH'])
# @requires_auth('patch:drinks')
# def update_drinks(jwt, id):
#     drink = Drink.query.get(id)

#     if not drink:
#         abort(404)
#     else:
#         try:

#             data = request.get_json()

#             title = data.get('title')
#             recipe = data.get('recipe')

#             if title:
#                 drink.title = title
#             if recipe:
#                 drink.title = recipe

#             drink.update()

#             return jsonify({
#                 'success': True,
#                 'drinks': [drink.long()]
#             })
#         except:
#             abort(422)


# @app.route("/drinks/<id>", methods=['DELETE'])
# @requires_auth('delete:drinks')
# def delete_drink(jwt, id):

#     drink = Drink.query.get(id)

#     if not drink:
#         abort(404)
#     else:
#         try:
#             drink.delete()
#             return jsonify({
#                 'success': True,
#                 'delete': id
#             })
#         except:
#             abort(422)

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