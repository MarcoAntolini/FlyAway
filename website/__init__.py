from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    
    db.init_app(app)
    from .models import User
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
            
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.welcome"
    login_manager.refresh_view = "auth.welcome"
    login_manager.remember_cookie_duration = timedelta(minutes=30)
    login_manager.session_protection = "strong"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app