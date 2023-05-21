from flask import Flask
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
    app.config["SECRET_KEY"] = "test"
    UPLOAD_FOLDER = "/uploads"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    db = PyMongo(app).db

    from .views import views
    from .auth import auth
    from .features import features

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
    app.register_blueprint(features,url_prefix="/services")

    return app
