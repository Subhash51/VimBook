from flask import Flask,request,jsonify,flash
from flask import render_template
from flask_pymongo import PyMongo
import hashlib

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/bookStore'
mongo = PyMongo(app)

@app.route('/')
def home():
    collection1=mongo.db.UserDetail
    collection2=mongo.db.books
    return render_template('index.html', title='Home')

@app.route('/signIn')
def signIn():
    return render_template('SignIn.html',title='Signing')

@app.route('/register')
def register():
    return render_template('Rsgtr.html',title="registering")

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'password': hashlib.sha256(request.form['password'].encode()).hexdigest()
        }

        collection = mongo.db.UserDetails
        result = collection.insert_one(data)
    return render_template("index2.html" , uname=data.get("name"))

@app.route('/checkUserInDb',methods=['POST'])
def checkUserInDb():
    if request.method =='POST':
        userName=request.form.get('email')
        userPassword=request.form.get('password')
    
        hashed_password = hashlib.sha256(userPassword.encode()).hexdigest()

        collection=mongo.db.UserDetails;
        tempUser=collection.find_one({'email':userName , 'password':userPassword })
        if not tempUser:
            giveAlert=True
            return render_template('SignIn.html',giveAlert=giveAlert)
        else:
            return render_template('index2.html',uname=tempUser.get("name"))

@app.route('/logout')
def logout():
    return render_template('index.html')


# Books Route 

@app.route('/Poetry')
def Poetry():
    collection = mongo.db.Books
    data = collection.find({"category": "poetry_books"})
    books = [book for book in data] 
    for book in books:
        if '_id' in book:
            book['_id'] = str(book['_id'])
    if not books:
        return "Data Not Found"
    return render_template("books/viewed.html", arr=books,category="poetry_books")

@app.route('/Novel')
def Novel():
    collection = mongo.db.Books
    data = collection.find({"category": "novels"})
    books = [book for book in data] 
    for book in books:
        if '_id' in book:
            book['_id'] = str(book['_id'])
    if not books:
        return "Data Not Found"
    return render_template("books/viewed.html", arr=books ,category="novels")

@app.route('/Comic')
def Comic():
    collection = mongo.db.Books
    data = collection.find({"category": "comic_books"})
    books = [book for book in data] 
    for book in books:
        if '_id' in book:
            book['_id'] = str(book['_id'])
    if not books:
        return "Data Not Found"
    return render_template("books/viewed.html", arr=books,category="comic_books")


@app.route('/Child')
def Child():
    collection = mongo.db.Books
    data = collection.find({"category": "children_books"})
    books = [book for book in data] 
    for book in books:
        if '_id' in book:
            book['_id'] = str(book['_id'])
    if not books:
        return "Data Not Found"
    return render_template("books/viewed.html", arr=books ,category="children_books")


@app.route('/Cook')
def Cook():
    collection = mongo.db.Books
    data = collection.find({"category": "cooking_books"})
    books = [book for book in data] 
    for book in books:
        if '_id' in book:
            book['_id'] = str(book['_id'])
    if not books:
        return "Data Not Found"
    return render_template("books/viewed.html", arr=books,category="cooking_books")


@app.route('/coffeeTable')
def coffeeTable():
    collection = mongo.db.Books
    data = collection.find({"category": "coffee_table_books"})
    books = [book for book in data] 
    for book in books:
        if '_id' in book:
            book['_id'] = str(book['_id'])
    if not books:
        return "Data Not Found"
    return render_template("books/viewed.html", arr=books, category="coffee_table_books")


@app.route('/search',methods=['POST'])
def search():
    if request.method=="POST":
        query=request.form.get("search")
        typeBook=request.form.get("typebook")

        collection = mongo.db.Books
        data = collection.find({
            "name": {"$regex": query},
            "category": {"$regex": typeBook}
        })
        books = [book for book in data] 
        for book in books:
            if '_id' in book:
                book['_id'] = str(book['_id'])
        if not books:
            return typeBook
        return render_template("books/viewed.html", arr=books)


if __name__ == "__main__":
    app.run(debug=True)
