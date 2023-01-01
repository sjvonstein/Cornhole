from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
DB_NAME = "cornhole"


def create_app():
    app = Flask(__name__)
    #app.config["SECRET_KEY"] = "dgf987324lkjsdef098lkjadf"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:h4decAsT@localhost/cornhole"
    #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    if not 'WEBSITE_HOSTNAME' in os.environ:
        # local development, where we'll use environment variables
        print("Loading config.development and environment variables from .env file.")
        app.config.from_object('website.development')
    else:
        # production
        print("Loading config.production.")
        app.config.from_object('website.production')

    app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY=app.config.get('SECRET_KEY'),
)
    
    
    
    
    db.init_app(app)
    migrate = Migrate(app, db)
    from .views import views

    app.register_blueprint(views, url_prefix="/")

    with app.app_context():
        db.create_all()

    return app