"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Users #, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_people():

    all_people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))

    print('GET Request: All the Users ====>', all_people)

    return jsonify(all_people), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():

    all_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))

    print('GET Request: All the Users ====>', all_planets)

    return jsonify(all_planets), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):

    people = People.query.get(people_id)
    people = people.serialize()

    print('GET Request: All the people ====>', people)

    return jsonify(people), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):

    planet = Planets.query.get(planet_id)
    planet = planet.serialize()

    print('GET Request: All the planets ====>', planet)

    return jsonify(planet), 200

@app.route('/users', methods=['GET'])
def get_all_users():

    all_users = Users.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))

    print('GET Request: All the Users ====>', all_users)

    return jsonify(all_users), 200

# @app.route('/users/favorites', methods=['GET'])
# def get_favorites():

#     favorites = Favorites.query.all()
#     favorites = favorites.serialize()
#     print(favorites)
#     print('GET Request: Favorites ====>', favorites)

#     return jsonify(favorites), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
