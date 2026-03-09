from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

def db():
    return sqlite3.connect("users.db")

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("loading.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = hash_password(request.form["password"])

        database = db()
        cursor = database.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=? AND verified=1",
        (email,password))

        user = cursor.fetchone()
        if user:
            session["user"] = email
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = hash_password(request.form["password"])

        database = db()
        cursor = database.cursor()

        cursor.execute(
        "INSERT INTO users(email,password,verified,admin) VALUES(?,?,0,0)",
        (email,password))

        database.commit()

        token = serializer.dumps(email, salt="verify")
        link = f"http://127.0.0.1:5000/verify/{token}"

        msg = Message(
        "Prisma Email Bestätigung",
        sender=config.MAIL_USERNAME,
        recipients=[email]
        )
        msg.body = f"Klicke auf den Link:\n{link}"
        mail.send(msg)

        return "Bestätigungs Email gesendet"

    return render_template("register.html")

@app.route("/verify/<token>")
def verify(token):
    email = serializer.loads(token, salt="verify", max_age=3600)
    database = db()
    cursor = database.cursor()
    cursor.execute("UPDATE users SET verified=1 WHERE email=?", (email,))
    database.commit()
    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")

@app.route("/forgot", methods=["GET","POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        token = serializer.dumps(email, salt="reset")
        link = f"http://127.0.0.1:5000/reset/{token}"

        msg = Message(
        "Passwort zurücksetzen",
        sender=config.MAIL_USERNAME,
        recipients=[email]
        )
        msg.body = f"Setze dein Passwort zurück:\n{link}"
        mail.send(msg)
        return "Reset Email gesendet"

    return render_template("forgot.html")

@app.route("/reset/<token>", methods=["GET","POST"])
def reset(token):
    email = serializer.loads(token, salt="reset", max_age=3600)
    if request.method == "POST":
        password = hash_password(request.form["password"])
        database = db()
        cursor = database.cursor()
        cursor.execute(
        "UPDATE users SET password=? WHERE email=?",
        (password,email)
        )
        database.commit()
        return redirect("/login")

    return render_template("reset.html")

@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")

    database = db()
    cursor = database.cursor()
    cursor.execute("SELECT admin FROM users WHERE email=?", (session["user"],))
    if cursor.fetchone()[0] != 1:
        return "Kein Zugriff"

    cursor.execute("SELECT email,verified,admin FROM users")
    users = cursor.fetchall()

    return render_template("admin.html", users=users)

app.run(debug=True)