import os


from flask import Flask, session, render_template,url_for,request,redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from argon2 import PasswordHasher

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

ph = PasswordHasher()

@app.route("/")
def index():
    if session.get('user'):
        return redirect(url_for("logged"))
    return render_template("index.html")

@app.route("/registrate")
def registrate():
    return render_template("registrate.html")

@app.route("/registration",methods=["POST"])
def registration():
    name=request.form.get("first") + " " + request.form.get("last")
    email=request.form.get("email")
    account=request.form.get("login")
    passwd=request.form.get("pass")
    hash=ph.hash(passwd)
    db.execute("INSERT INTO users (account,hash,name,email) VALUES (:account,:hash,:name,:email)",
                {"account": account,"hash": hash,"name": name,"email": email})
    db.commit()
    return render_template("registration.html")

@app.route("/login",methods=["POST"])
def login():
    account=request.form.get("login")
    passwd=request.form.get("pass")

    users=db.execute("SELECT * FROM users WHERE account= :account",
        {"account": account}).fetchall()
    for user in users:
        try:
            if ph.verify(user.hash,passwd):
                session["user"]=user
                return redirect(url_for("logged"))
        except:
            return redirect(url_for("index"))

    return "NO JOY :()"

@app.route("/logged")
def logged():
    if session.get('user') == None:
        return redirect(url_for("index"))
    return render_template("logged.html",user=session.get('user'))

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route("/search",methods=["POST"])
def search():
    if session.get('user') == None:
        return redirect(url_for("index"))
    search_for=request.form.get("search_for");
    books=db.execute("SELECT * FROM books WHERE isbn LIKE :search_for OR name LIKE :search_for OR author LIKE :search_for",
        {"search_for": "%" + search_for + "%"}).fetchall()
    return render_template("logged.html",user=session.get('user'),books=books,searched=True)

@app.route("/details/<int:book_id>")
def details(book_id):
    if session.get('user') == None:
        return redirect(url_for("index"))
    user=session.get('user').user_id
    book=db.execute("SELECT * FROM books WHERE book_id=:book_id",
        {"book_id": book_id}).fetchone()
    reviews=db.execute("SELECT * FROM reviews WHERE book=:book_id",
        {"book_id": book_id}).fetchall()
    reviewed=db.execute("SELECT COUNT(*) FROM reviews WHERE book=:book_id AND userid=:user",
        {"book_id": book_id,"user": user}).fetchone()
    return render_template("details.html",book=book,reviews=reviews,reviewed=reviewed[0])

@app.route("/add_review",methods=["POST"])
def add_review():
    if session.get('user') == None:
        return redirect(url_for("index"))
    review=request.form.get("review")
    rating=request.form.get("rating")
    user_id=request.form.get("user_id")
    book=request.form.get("book_id")
    db.execute("INSERT INTO reviews (book,userid,rating,review) VALUES(:book, :user_id, :rating, :review)",
        {"book": book, "user_id": user_id, "rating": rating, "review": review})
    db.commit()
    return redirect(url_for("details",book_id=book))
