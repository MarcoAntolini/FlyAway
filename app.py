from flask import Flask, render_template, request, send_file, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from bs4 import BeautifulSoup
from datetime import timedelta
import bcrypt
import json

app = Flask(__name__)  # used for debugging purposes
app.secret_key = "super secret"  # used for debugging purposes

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "welcome"

# create a class for our user model
class User(UserMixin):
    users = []
    i = 0
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @classmethod
    def add_user(cls, user):
        cls.users.append(user)
        user.id = cls.i
        cls.i+=1

    @classmethod
    def get(cls, user_id: int) -> "User":
        for user in cls.users:
            if user.id == user_id:
                return user
        return None


# create a callback function for flask_login
# It takes a user ID as an argument and should return the corresponding user object, or None if the user does not exist:
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode(), hashed_password)


def save_user(username, password):
    users = {}
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        pass
    hashed_password = hash_password(password)
    users[username] = hashed_password.decode()
    with open("users.json", "w") as f:
        json.dump(users, f)


def check_user(username, password):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            if username in users:
                hashed_password = users[username].encode()
                return check_password(password, hashed_password)
            else:
                return False
    except:
        return False


def user_exists(username):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            return username in users
    except:
        return False


@app.before_request
def remember_last_page():
    session["last_page"] = request.url


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "GET":
        return render_template("welcome.html", nav=NAV)
    elif request.method == "POST":
        button_class = request.form.get("class")
        # if the button is register:
        if button_class == "register":
            username = request.form["username"]
            password = request.form["password"]
            # if the username already exists:
            if user_exists(username):
                error_msg = error_register
                return render_template("welcome.html", nav=NAV, error=error_msg)
            # if the username doesn't exist:
            save_user(username, password)
            new_user = User(username, username)
            User.add_user(new_user)
            login_user(new_user, remember=True)
            is_logged = logged_y
            return render_template("index.html", nav=NAV, logged=is_logged)
        # if the button is login:
        elif button_class == "login":
            username = request.form["username"]
            password = request.form["password"]
            # if the username and password are correct:
            if check_user(username, password):
                user = User(username, username)
                login_user(user, remember=True)
                is_logged = logged_y
                return render_template("index.html", nav=NAV, logged=is_logged)
            # if the username and password are incorrect:
            error_msg = error_login
            return render_template("welcome.html", nav=NAV, error=error_msg)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    is_logged = logged_n
    return redirect(url_for("index"), nav=NAV, logged=is_logged)


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
