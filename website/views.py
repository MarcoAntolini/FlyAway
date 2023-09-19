from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from .consts import NAV, logged_class_yes, logged_class_no, index_url


views = Blueprint("views", __name__)


@views.route("/services", methods=["GET"])
@login_required
def services():
    return render_template("services.html", nav=NAV)


@views.route("/", methods=["GET"])
@views.route("/index", methods=["GET"])
def index():
    if current_user.is_authenticated:
        logged_class = logged_class_yes
    else:
        logged_class = logged_class_no
    return render_template(index_url, nav=NAV, logged=logged_class)


@views.route("<template>")
def load_template(template):
    try:
        if not template.endswith(".html"):
            template += ".html"
        return render_template(template, nav=NAV)
    except TemplateNotFound:
        return render_template("404.html"), 404
    except Exception:
        return render_template("500.html"), 500


@views.route("/static/report/Report.pdf", methods=["GET"])
def download():
    return send_file("static/report/Report.pdf", as_attachment=True)
