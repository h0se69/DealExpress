from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3, os
from os import path

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
    db.init_app(app)

    from .routes import routes
    app.register_blueprint(routes, url_prefix ='/')
    
    with app.app_context():
        db.create_all()
    return app


# Init Database
# 
# 
# 
# 

#from DealExpress import routes
from DealExpress.APIs import *