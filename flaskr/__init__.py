from dotenv import load_dotenv
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# pass subclass of DeclarativeBase into the constructor
# Ref: https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/
class Base(DeclarativeBase):
    pass

# Initialise the db object, ie the instance of SQLAlchemy
db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    
    # Load environment variables from the .env file
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        API_KEY=os.getenv('API_KEY'),
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        # Create a data.db file in the instance folder
        SQLALCHEMY_DATABASE_URI = "sqlite:///instance/data.db",
        SQLALCHEMY_TRACK_NOTIFICATIONS = False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    # @app.route('/')
    # def hello():
    #     return 'Welcome to SkyApp'

    # tie the db to the Flask app
    db.init_app(app)

    from .models import User, Post, Nasa
    # Reference model classes to eliminate unused import warning
    __all__ = [User, Post, Nasa]

    # Context required to initialise dbs as not in a session
    with app.app_context():
        db.create_all()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import apod
    app.register_blueprint(apod.bp)

    return app