from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Mail config (optional anpassen)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_password"

mail = Mail(app)

# Login Form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")


@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Beispiel Login Check
        if email == "admin@test.com" and password == "123456":
            flash("Login erfolgreich!")
            return redirect(url_for("dashboard"))
        else:
            flash("Falsche Login-Daten")

    return render_template("index.html", form=form)


@app.route("/dashboard")
def dashboard():
    return "Willkommen im Dashboard!"


# WICHTIG für Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
