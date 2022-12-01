from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3, os
from os import path
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
#flaskObj = Flask(__name__)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'you-will-never-guess',
        # where to store app.db (database file)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    from .models import User
    login_manager = LoginManager(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    db.init_app(app)
    from .routes import routes
    app.register_blueprint(routes, url_prefix ='/')
    
    with app.app_context():
        db.create_all()
    return app

#from DealExpress import routes
from DealExpress.APIs import *