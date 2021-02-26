import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movies, Actors

assistant_token = "Bearer {}".format(os.environ.get('ASSISTANT_TOKEN'))
director_token = "Bearer {}".format(os.environ.get('DIRECTOR_TOKEN'))
producer_token = "Bearer {}".format(os.environ.get('PRODUCER_TOKEN'))

class CastingAgencyTests(unittest.TestCase):

  def setUp(self):
    # define test variables and initialize app
    self.app = app
    self.client = self.app.test_client
    self.database_name = "casting_test"
    self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
    setup_db(self.app)

    self.new_actor = {
      'name': 'Rashida Jones',
      'age': '34',
      'gender': 'Female'
    }

    self.update_actor = {
      'name': 'Dwight Schrute',
      'age': '42',
      'gender': 'Male'
    }

    self.new_movie = {
      'title': 'Avengers 2',
      'release_date': '2010'
    }

    self.update_movie = {
      'title': 'Spongebob The Movie',
      'release_date': '2008'
    }

    # tie app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

  def tearDown(self):
    """Executed after reach test"""
    pass

  # test 200 response for all enpoints (movies and actors db)
  def test_get_actors (self):
    response = self.client().get('/actors', headers = {"Authorization": (assistant_token)})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(data['actors'])

  def test_get_movies (self):
    response = self.client().get('/movies', headers= {"Authorization": (assistant_token)})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(data['movies'])

  def test_create_actors (self):
    response = self.client().post('/actors', json=self.new_actor, headers = {"Authorization": (director_token)})
    data = json.loads(response.data)

    self.assertTrue(data['success'])
    self.assertTrue(data['actor'])

  def test_create_movies (self):
    response = self.client().post('/movies', json=self.new_movie, headers = {"Authorization": (producer_token)})
    data = json.loads(response.data)

    self.assertTrue(data['success'])
    self.assertTrue(data['movie'])

  def test_update_actors (self):
    self.client().post('/actors', json=self.new_actor, headers = {"Authorization": (producer_token)})
    response = self.client().patch('/actors/5', json=self.update_actor, headers= {"Authorization": (producer_token)})
    data = json.loads(response.data)

    self.assertTrue(data['success'])
    self.assertTrue(data['actors'])

  def test_update_movies (self):
    self.client().post('/movies', json=self.new_movie, headers={ "Authorization": (director_token)})
    response = self.client().patch('/movies/5', json=self.update_movie, headers={ "Authorization": (director_token)})
    data = json.loads(response.data)

    self.assertTrue(data['success'])
    self.assertTrue(data['movies'])

  def test_delete_actors (self):
    self.client().post('/actors', json=self.new_actor, headers={ "Authorization": (producer_token)})
    response = self.client().delete('/actors/4', headers={ "Authorization": (producer_token)})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['delete'], '4')
    self.assertTrue(data['success'])

  def test_delete_movies (self):
    self.client().post('/movies', json=self.new_movie, headers={ "Authorization": (producer_token)})
    response = self.client().delete('/movies/4', headers={ "Authorization": (producer_token)})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['delete'], '4')
    self.assertTrue(data['success'])

  # test 400 and 401 response on all endpoints for movies and actors db
  def test_401_get_actors (self):
    response = self.client().get('/actors')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 401)
    self.assertFalse(data['success'])

  def test_401_get_movies (self):
    response = self.client().get('/movies')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 401)
    self.assertFalse(data['success'])
  
  def test_401_create_actors (self):
    response = self.client().post('/actors', json=self.new_actor)
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 401)
    self.assertFalse(data['success'])

  def test_401_create_movies (self):
    response = self.client().post('/movies', json=self.new_movie)
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 401)
    self.assertFalse(data['success'])

  def test_404_update_actors (self):
    response = self.client().patch('/actors/1000', json=self.update_actor, headers={ "Authorization": (producer_token)})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertFalse(data['success'])

  def test_404_update_movies (self):
    response = self.client().patch('/movies/1000', json=self.update_movie, headers={"Authorization": (producer_token)})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertFalse(data['success'])
  
  def test_404_delete_actors (self):
    response = self.client().delete('/actors/1000', headers={ "Authorization": (producer_token)})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertFalse(data['success'])
  
  def test_404_delete_movies (self):
    response = self.client().delete('/movies/1000', headers={ "Authorization": (producer_token)})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertFalse(data['success'])

# make the tests executible 
if __name__ == "__main__":
  unittest.main()