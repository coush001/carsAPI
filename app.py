import os
from flask import Flask
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import tools

# create the flask app
app = Flask(__name__)

# set the config aka dev / prod etc as seen in config.py : https://realpython.com/flask-by-example-part-1-project-setup/
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

# set up the postgres data base connection variables from ENV
POSTGRES_URL = tools.get_env_variable("POSTGRES_URL")
POSTGRES_USER = tools.get_env_variable("POSTGRES_USER")
POSTGRES_PW = tools.get_env_variable("POSTGRES_PW")
POSTGRES_DB = tools.get_env_variable("POSTGRES_DB")
POSTGES_PORT = tools.get_env_variable("POSTGRES_PORT")

# set config for sql alchemy to connect to postgres
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# create db object that is an sql alch object that is passed the app which has been configed for postgres connection
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
# set up migrations for database if needed
migrate = Migrate(app, db)

class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())
    hugo_col =db.Column(db.String())

    def __init__(self, name, model, doors, hugo_col):
        self.name = name
        self.model = model
        self.doors = doors
        self.hugo_col = hugo_col

    def __repr__(self):
        return f"<Car {self.name}>"

@app.route("/")
def index():
    secret_key = app.config.get("SECRET_KEY")
    return "Hello boss MAN 10!" + f"The URL IS :     postgres://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}:5432/{POSTGRES_DB}"


@app.route('/cars', methods=['POST'])
def post_car():
    data = request.get_json()
    new_car = CarsModel(name=data['name'], model=data['model'], doors=data['doors'], hugo_col=data['hugo_col'])
    db.session.add(new_car)
    db.session.commit()
    return {"message": f"car {new_car.name} has been created successfully."}


@app.route('/cars', methods=['GET'])
def get_cars():
    cars = CarsModel.query.all()
    results = [
        {
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        } for car in cars]
    return {"count": len(results), "cars": results}


@app.route('/cars/<car_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(car_id):
    car = CarsModel.query.get_or_404(car_id)

    if request.method == 'GET':
        response = {
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return {"message": "success", "car": response}

    elif request.method == 'PUT':
        data = request.get_json()
        car.name = data['name']
        car.model = data['model']
        car.doors = data['doors']
        db.session.add(car)
        db.session.commit()
        return {"message": f"car {car.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return {"message": f"Car {car.name} successfully deleted."}