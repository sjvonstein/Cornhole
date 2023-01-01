from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DB_NAME = "cornhole"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dgf987324lkjsdef098lkjadf"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:h4decAsT@localhost/cornhole"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    with app.app_context():
        db.create_all()

    return app