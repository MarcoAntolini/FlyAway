from flask import Blueprint, render_template, request, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from .util import *


auth = Blueprint("auth", __name__)


@auth.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "GET":
        return render_template("welcome.html", nav=NAV)
    elif request.method == "POST":
        submit_type = request.form.get("submit_type")
        if submit_type == "register":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()
            if (user):
                error_msg = error_msg_register
                return render_template("welcome.html", nav=NAV, error=error_msg)
            else:
                new_user = User(username=username, password=generate_password_hash(password, method="sha256"))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                logged_class = logged_class_yes
                return render_template("index.html", nav=NAV, logged=logged_class)
        elif submit_type == "login":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()
            if (user):
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    logged_class = logged_class_yes
                    return render_template("index.html", nav=NAV, logged=logged_class)
                else:
                    error_msg = error_msg_login_password
                    return render_template("welcome.html", nav=NAV, error=error_msg)
            else:
                error_msg = error_msg_login_username
                return render_template("welcome.html", nav=NAV, error=error_msg)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    logged_class = logged_class_no
    return render_template("index.html", nav=NAV, logged=logged_class)


@auth.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@auth.errorhandler(500)
def server_not_working(e):
    return render_template("500.html"), 500