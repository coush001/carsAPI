import os
from flask import Flask
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cars_api"
db = SQLAlchemy(app)
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
    return "Hello boss MAN 10!"