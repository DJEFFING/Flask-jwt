from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app = app) # Initialisation de la base de donnée
    bcrypt.init_app(app = app) # Initialisation du Bcrypt

    from auth_routes import auth
    from main_routes import main
    
    app.register_blueprint(auth)
    app.register_blueprint(main)


    return app