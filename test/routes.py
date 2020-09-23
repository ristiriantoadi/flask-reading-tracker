from flask import render_template,url_for,flash,redirect,request,session,send_from_directory
from test import app, mongo
import os
from bson.objectid import ObjectId
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

@app.route('/buku/hapus/<id>',methods=['GET']) 
def hapus_buku(id):
    if 'username' in session:
        booksCollection = mongo.db.books
        book=booksCollection.find_one({'_id':ObjectId(str(id))})
        booksCollection.remove(book)
        return redirect(url_for('index'))
        
@app.route('/buku/edit/<id>',methods=['GET','POST']) 
def edit_buku(id):
    if 'username' in session:
        if request.method == "POST":
            
            judul = request.form['judul']
            pengarang = request.form['pengarang']
            mulaiBaca = request.form['mulai-baca']
            jumlahHalaman = request.form['jumlah-halaman']
            deskripsi = request.form['deskripsi']
            status = request.form['status']

            books = mongo.db.books
            book=books.find_one({'_id':ObjectId(str(id))})
            book['judul'] = judul
            book['pengarang'] = pengarang
            book['mulaiBaca'] = mulaiBaca
            book['deskripsi'] = deskripsi
            book['status'] = status
            book['jumlahHalaman'] = jumlahHalaman
            books.save(book)
            return redirect(url_for('index'))
        
        books = mongo.db.books
        book=books.find_one({'_id':ObjectId(str(id))})

        return render_template("edit buku.html",username=session['username'],book=book)

@app.route('/buku/tambah',methods=['GET', 'POST']) 
def tambah_buku():
    if 'username' in session:
        if request.method=="POST":
            judul = request.form['judul']
            pengarang = request.form['pengarang']
            mulaiBaca = request.form['mulai-baca']
            jumlahHalaman = request.form['jumlah-halaman']
            deskripsi = request.form['deskripsi']
            status = request.form['status']

            file = request.files['cover']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                books = mongo.db.books
                books.insert({'username':session['username'],
                        'judul':judul,
                        'pengarang':pengarang,
                        'mulaiBaca':mulaiBaca,
                        'deskripsi':deskripsi,
                        'status':status,
                        'jumlahHalaman':jumlahHalaman,
                        'cover':filename})
                return redirect(url_for('index'))

        return render_template("tambah buku.html",username=session['username'])
    return redirect(url_for('login')) 

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
