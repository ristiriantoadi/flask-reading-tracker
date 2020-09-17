from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY']='49e244cf65248712dc2ce77e4196f012'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)

from test import routes