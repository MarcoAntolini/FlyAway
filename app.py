from flask import Flask, render_template, request, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from jinja2 import TemplateNotFound
from bs4 import BeautifulSoup
from datetime import timedelta
import requests

app = Flask(__name__)  # used for debugging purposes

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


NAV = [
    ("Home", "/"),
    ("About Us", "/about"),
    ("Services", "/services"),
    ("Privacy & Cookies", "/privacy-policy"),
    ("Terms & Conditions", "/terms-and-conditions"), 
]
                

logged_y = "logged"
logged_n = "notLogged"
is_logged = ""

error_login = "Invalid username or password"
error_register = "Username already exists"
error_msg = ""


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    return render_template("welcome.html", nav=NAV)
    # html = requests.get("http://127.0.0.1:5000/")
    # soup = BeautifulSoup(html.text, "html.parser")
    # check_button = soup.find("input", id="switch")
    # if check_button.has_class("register"):  # if the button is register
    #     if request.method != "POST":
    #         return render_template("welcome.html", nav=NAV)
    #     username = request.form["username"]
    #     password = request.form["password"]
    #     for user in users:
    #         if user.username == username:
    #             error_msg = error_register
    #             return render_template("welcome.html", nav=NAV, error=error_msg)
    #     new_user = User(len(users), username, password)
    #     users.append(new_user)
    #     login_user(new_user, remember=True, duration=timedelta(days=30))
    #     is_logged = logged_y
    #     return render_template("index.html", nav=NAV, logged=is_logged)
    # elif check_button.has_class("login"):  # if the button is login
    #     if request.method != "POST":
    #         return render_template("welcome.html", nav=NAV)
    #     username = request.form["username"]
    #     password = request.form["password"]
    #     for user in users:
    #         if user.username == username and user.password == password:
    #             login_user(user, remember=True, duration=timedelta(days=7))
    #             is_logged = logged_y
    #             return render_template("index.html", nav=NAV, logged=is_logged)
    #     error_msg = error_login
    #     return render_template("welcome.html", nav=NAV, error=error_msg)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    is_logged = logged_n
    return render_template("index.html", nav=NAV, logged=is_logged)


@app.route("/services", methods=["GET"])
@login_required
def services():
    return render_template("services.html", nav=NAV, logged=is_logged)


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    is_logged = logged_y
    return render_template("index.html", nav=NAV, logged=is_logged)


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html", nav=NAV)


@app.route("/privacy-policy", methods=["GET"])
def privacy():
    return render_template("privacy-policy.html", nav=NAV)


@app.route("/terms-and-conditions", methods=["GET"])
def terms():
    return render_template("terms-and-conditions.html", nav=NAV)


@app.route("/static/report/Report.pdf", methods=["GET"])
def download():
    return send_file("static/report/Report.pdf", as_attachment=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_not_working(e):
    return render_template("500.html"), 500


# create a callback function for flask_login
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None
