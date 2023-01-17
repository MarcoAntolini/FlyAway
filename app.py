from flask import Flask, render_template, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from jinja2 import TemplateNotFound
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

# import os
# os.environ["no_proxy"] = "127.0.0.1,localhost"

# url = "http://127.0.0.1:5000/"
# page = open(url)
# soup = BeautifulSoup(page.read())


isLogged = "notLogged"


def switch_logged():
    global isLogged
    if isLogged == "notLogged":
        isLogged = "logged"
    else:
        isLogged = "notLogged"
    return isLogged


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    html = requests.get("http://localhost:5000/")
    soup = BeautifulSoup(html.text, "lxml")
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
        return render_template("index.html", logged=switch_logged())
    elif check_button.has_class("login"):  # if the button is login
        if request.method != "POST":
            return render_template("welcome.html")
        username = request.form["username"]
        password = request.form["password"]
        for user in users:
            if user.username == username and user.password == password:
                login_user(user, remember=True, duration=timedelta(days=7))
                return render_template("index.html", logged=switch_logged())
        return render_template("welcome.html", error="Invalid username or password")


# create a logout page
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return render_template("index.html", logged=switch_logged())


@app.route("/services", methods=["GET"])
@login_required
def services():
    return render_template("services.html")


@app.route("/")
def index():
    global isLogged
    return render_template("index.html", logged=isLogged)


@app.route("/<path>")
def pages():
    try:
        if not path.endswith(".html"):
            path += ".html"
        return render_template(path)
    except TemplateNotFound:
        return render_template("404.html"), 404
    except:
        return render_template("500.html"), 500


@app.route("/static/report/Report.pdf", methods=["GET"])
def download():
    return send_file("static/report/Report.pdf", as_attachment=True)


# create a callback function for flask_login
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None
