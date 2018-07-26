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
