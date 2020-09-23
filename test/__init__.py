from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config['SECRET_KEY']='49e244cf65248712dc2ce77e4196f012'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)),"static","cover")
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/readingtracker"
mongo = PyMongo(app)

from test import routes