from flask import render_template,url_for,flash,redirect,request,session
from test import app, mongo
import os
# from .models import User,Post

@app.route('/login',methods=['GET', 'POST']) 
def login():
    if request.method == "POST":
        # return "yes"
        username=request.form['username']
        password=request.form['password']
        usersCollection = mongo.db.users
        user=usersCollection.find_one({'username':username,'password':password})
        # user = usersCollection.find_one({'$or':[{'username':username,'password':password},{'username':'ristirianto'}]})
        if user is not None:
            session['username'] = user['username']
            return redirect(url_for('index'))
        flash(f'username/password salah','danger')
        return redirect(url_for('login'))    
    return render_template("login.html",title="ReadingTracker | Login")

@app.route('/logout') 
def logout():
     # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register',methods=['GET', 'POST']) 
def register(): 
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']

        userCollection = mongo.db.users

        user=userCollection.find_one({'username':username})
        if user is not None:
            flash(f'Username sudah terpakai','danger')
            return render_template("register.html")
        userCollection.insert({'username':username,'password':password})
        session['username'] = username
        return redirect(url_for('index'))
    return render_template("register.html", title="ReadingTracker | Register")

@app.route('/') 
def index(): 
    if 'username' in session:
        # return "logged in as "+session['username']
        books=[{ 
            'title' : 'Boneshaker',
            'author' : 'lorem ipsum',
            'pages' : 250,
            'start_reading' : '11/10/2020',
            'status' : 'Sedang dibaca'
            }, 
            { 
            'title' : 'Harry Potter',
            'author' : 'J.K Rowling',
            'pages' : 400,
            'start_reading' : '11/9/2020',
            'status' : 'Sudah dibaca'
            }] 
        booksCollection = mongo.db.books
        books = booksCollection.find({'username':session['username']})
        return render_template("index.html",username=session['username'],books=books)
    return redirect(url_for('login'))

@app.route('/tambah_buku',methods=['GET', 'POST']) 
def tambah_buku():
    if 'username' in session:
        if request.method=="POST":
            judul = request.form['judul']
            pengarang = request.form['pengarang']
            mulaiBaca = request.form['mulai-baca']
            deskripsi = request.form['deskripsi']
            status = request.form['status']

            file = request.files['cover']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                books = mongo.db.books

            # user=userCollection.find_one({'username':username})
            # if user is not None:
            #     flash(f'Username sudah terpakai','danger')
            #     return render_template("register.html")
                books.insert({'username':session['username'],
                        'judul':judul,
                        'pengarang':pengarang,
                        'mulaiBaca':mulaiBaca,
                        'deskripsi':deskripsi,
                        'status':status,
                        'cover':filename})
            # app.logger.info('Mulai baca '+str(mulaiBaca))
        return render_template("tambah buku.html",username=session['username'])
    return redirect(url_for('login')) 


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
