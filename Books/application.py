import os
#import bcrypt
import requests
from collections import OrderedDict

from flask import Flask, session, render_template, request, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/home")
def test():
    return "running"


@app.route("/", methods=["GET", "POST"])
def index():
    msg = ""
    if session["user_id"] == None:
        if request.method == "POST":
            uname = request.form.get("username")
            password = request.form.get("password")
            data = db.execute(f"SELECT user_id, username, password FROM users WHERE username='{uname}'").fetchall()
            if len(data) != 0: 
                session["user_id"] = data[0][0]
                if password != data[0][2]:
                    msg = "password incorrect"
            else:
                msg = "user not found"
            return render_template("login.html", msg=msg)
        else:
            msg = "please login"
    else:
        msg = f"You are logged in as user {session['user_id']}"
    return render_template("login.html", msg = msg)


@app.route("/logout")
def logout():
    msg =""
    if session["user_id"] != None:
        session["user_id"] = None
        msg = "Logout Successfull"
    else:
        msg ="Please login before logging out!"
    return render_template("login.html", msg=msg)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        uname = request.form.get("username")
        password = request.form.get("password")
        exist = db.execute(f"SELECT * FROM users WHERE username='{uname}';").fetchall()
        if len(exist) != 0: 
            return render_template("register.html", msg="Users already exists")
        db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)", {"name": name, "username":uname, "password": password})
        db.commit()
        return "Successfully Registered!"
    return render_template("register.html")


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if session["user_id"] != None:
        if (data := db.execute(f"SELECT * FROM books WHERE ISBN like '%{query}%' LIMIT 20;").fetchall()):
            return render_template("search.html", data=data)
        if (data := db.execute(f"SELECT * FROM books WHERE author like '%{query}%' LIMIT 20").fetchall()):
            return render_template("search.html", data=data)
        if (data := db.execute(f"SELECT * FROM books WHERE title like '%{query}%' LIMIT 20").fetchall()):
            return render_template("search.html", data=data)
        if len(data) == 0:
            return render_template("login.html", err="No result found")
    return render_template("login.html", err="Please Login")


@app.route("/book/<string:name>", methods=["GET", "POST"])
def details(name):
    msg=""
    data = db.execute(f"SELECT * FROM books WHERE title='{name}';").fetchall()
    reviews = db.execute(f"SELECT users.user_id, username, rating, text_review FROM reviews JOIN users ON users.user_id = reviews.user_id JOIN books ON books.isbn = reviews.isbn WHERE books.ISBN = '{data[0][0]}';").fetchall()
    if request.method == "POST":
        if session["user_id"] not in [i[0] for i in reviews]:
            star_rating = request.form.get("star-rating")
            text_review = request.form.get("text-review")
            db.execute("INSERT INTO reviews (user_id, ISBN, rating, text_review) VALUES(:user_id, :ISBN, :rating, :text_review)", {"user_id": session["user_id"], "ISBN": data[0][0], "rating": star_rating, "text_review": text_review})
            db.commit()
            reviews = db.execute(f"SELECT users.user_id, username, rating, text_review FROM reviews JOIN users ON users.user_id = reviews.user_id JOIN books ON books.isbn = reviews.isbn WHERE books.ISBN = '{data[0][0]}';").fetchall()
        else:
            msg = "You've already reviewed"
    key = "mIsKW7MtvLXzYFxcggqnvQ"
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"KEY": key, "isbns": data[0][0]}) 
    return render_template("book.html", data=data, avg_rating=res.json()["books"][0]["average_rating"], total_rating=res.json()["books"][0]["reviews_count"], reviews=reviews, msg=msg)




@app.route("/api/<string:isbn>")
def api(isbn):
    if (data := db.execute(f"SELECT books.title, books.author, books.year, reviews.ISBN, rating FROM reviews JOIN books ON books.isbn=reviews.isbn WHERE reviews.ISBN='{isbn}';").fetchall()):
        reviews_count = len(data)
        avg = sum([i[4] for i in data])/reviews_count
        data = data[0]
        json_content = OrderedDict()
        json_content["title"] = data[0]
        json_content["author"] = data[1]
        json_content["year"] = data[2]
        json_content["isbn"] = data[3]
        json_content["review_count"] = reviews_count
        json_content["average_score"] = avg
#        data = {"title": data[0], "author": data[1], "year": data[2], "isbn": data[3], "review_count": reviews_count, "average_score": avg}
        return json_content 
    return "404 Error"

'''
@app.route("/api/<string:isbn>")
def api(isbn):
    if (data := db.execute(f"SELECT books.title, books.author, books.year, reviews.ISBN, rating FROM reviews JOIN books ON books.isbn=reviews.isbn WHERE reviews.ISBN='{isbn}';").fetchall()):
        reviews_count = len(data)
        avg = sum([i[4] for i in data])/reviews_count
        data = data[0]
        data = {"title": data[0], "author": data[1], "year": data[2], "isbn": data[3], "review_count": reviews_count, "average_score": avg}
        return jsonify(data)
    return "404 Error"
'''
