from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import mysql.connector
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

envuser = os.getenv("user")
envpassword = os.getenv("password")
envhost = os.getenv("host")

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app)
app.secret_key = "BRUHHH"


db = mysql.connector.connect(
    host=envhost,
    user=envuser,
    password=envpassword,
    database="information_dashboard"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        hashed = generate_password_hash(password)

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user (email, password) VALUES (%s, %s)",
            (email, hashed)
        )
        db.commit()
        cursor.close()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cursor = db.cursor()
        cursor.execute(
            "SELECT id, password FROM user WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["email"] = email
            return redirect("/")
        else:
            return "FEIL LOGIN RAHHHH"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("email", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
