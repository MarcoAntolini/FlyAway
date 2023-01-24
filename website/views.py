from flask import Blueprint, render_template, request, send_file, url_for
from flask_login import login_required
from .util import *


views = Blueprint("views", __name__)


@views.route("/services", methods=["GET"])
@login_required
def services():
    return render_template("services.html", nav=NAV)


@views.route("/", methods=["GET"])
@views.route("/index", methods=["GET"])
def index():
    return render_template("index.html", nav=NAV, logged=logged_class)


@views.route("/about", methods=["GET"])
def about():
    return render_template("about.html", nav=NAV)


@views.route("/privacy-policy", methods=["GET"])
def privacy():
    return render_template("privacy-policy.html", nav=NAV)


@views.route("/terms-and-conditions", methods=["GET"])
def terms():
    return render_template("terms-and-conditions.html", nav=NAV)


@views.route("/static/report/Report.pdf", methods=["GET"])
def download():
    return send_file("static/report/Report.pdf", as_attachment=True)


@views.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@views.errorhandler(500)
def server_not_working(e):
    return render_template("500.html"), 500