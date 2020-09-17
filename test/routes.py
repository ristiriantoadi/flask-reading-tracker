from flask import render_template,url_for,flash,redirect
from test import app, mongo
# from .models import User,Post

@app.route('/login') 
def login(): 
    return render_template("login.html")

@app.route('/register') 
def register(): 
    return render_template("register.html")

@app.route('/') 
def index(): 
    return render_template("index.html")
