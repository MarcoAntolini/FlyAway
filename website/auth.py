from flask import Blueprint, render_template, request, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from .consts import (
    NAV,
    logged_class_yes,
    logged_class_no,
    error_msg_register,
    error_msg_login_password,
    error_msg_login_username,
    index_url,
    welcome_url,
)


auth = Blueprint("auth", __name__)


@auth.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "GET":
        return render_template(welcome_url, nav=NAV)
    elif request.method == "POST":
        submit_type = request.form.get("submit_type")
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if submit_type == "register":
            if user:
                error_msg = error_msg_register
                return render_template(welcome_url, nav=NAV, error=error_msg)
            new_user = User(
                username=username,
                password=generate_password_hash(password, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            logged_class = logged_class_yes
            return render_template(index_url, nav=NAV, logged=logged_class)
        elif submit_type == "login":
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    logged_class = logged_class_yes
                    return render_template(index_url, nav=NAV, logged=logged_class)
                error_msg = error_msg_login_password
                return render_template(welcome_url, nav=NAV, error=error_msg)
            error_msg = error_msg_login_username
            return render_template(welcome_url, nav=NAV, error=error_msg)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    logged_class = logged_class_no
    return render_template(index_url, nav=NAV, logged=logged_class)


@auth.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@auth.errorhandler(500)
def server_not_working(e):
    return render_template("500.html"), 500
