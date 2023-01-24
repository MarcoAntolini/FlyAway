from website import create_app
from flask import render_template


app = create_app()


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_not_working(e):
    return render_template("500.html"), 500