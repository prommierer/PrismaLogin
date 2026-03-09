from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "secretkey"

users = {}

@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users and users[email] == password:
            return redirect("/dashboard")
        else:
            flash("Falsche Login Daten")

    return render_template("index.html")


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        users[email] = password

        flash("Registrierung erfolgreich")
        return redirect("/")

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return "<h1>Du bist eingeloggt 🎉</h1>"


if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
