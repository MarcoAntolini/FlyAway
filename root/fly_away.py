from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from bs4 import BeautifulSoup
from datetime import timedelta
import requests

app = Flask(__name__)
app.secret_key = "secret key"  # used for securing session data

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.session_protection = "strong"
login_manager.login_view = "welcome"

# create a class for our user model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# create a list to store our user data
users = []

html = requests.get(
    "https://www.flyaway.com.au/"
).text  # TODO: change to the actual website
soup = BeautifulSoup(html, "html.parser")


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    check_button = soup.find("input", id="switch")
    if check_button.has_class("register"):  # if the button is register
        if request.method != "POST":
            return render_template("welcome.html")
        username = request.form["username"]
        password = request.form["password"]
        for user in users:
            if user.username == username:
                return render_template("welcome.html", error="Username already exists")
        new_user = User(len(users), username, password)
        users.append(new_user)
        login_user(new_user, remember=True, duration=timedelta(days=30))
        return render_template("index.html", logged="logged")
    elif check_button.has_class("login"):  # if the button is login
        if request.method != "POST":
            return render_template("welcome.html")
        username = request.form["username"]
        password = request.form["password"]
        for user in users:
            if user.username == username and user.password == password:
                login_user(user, remember=True, duration=timedelta(days=7))
                return render_template("index.html", logged="logged")
        return render_template("welcome.html", error="Invalid username or password")


# create a logout page
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("index.html", logged="notLogged")


# create a protected page
@app.route("/services")
@login_required
def services():
    return render_template("services.html")


# create a callback function for flask_login
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None
