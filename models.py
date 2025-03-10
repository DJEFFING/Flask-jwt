from main import db,bcrypt
from flask_login import UserMixin
from datetime import datetime
import logging as lg


class User(db.Model, UserMixin):
    __tablename__ = "users"  # Spécification du nom de la table

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=True, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone_number = db.Column(
        db.String(15), nullable=False, unique=True
    )  # Utilisation d'un String pour le téléphone
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    password = db.Column(db.String(80), nullable=False)
    profil_url = db.Column(
        db.String(255), nullable=True
    )  # Peut être nullable si pas d'URL au départ
    description = db.Column(
        db.Text, nullable=True
    )  # Utilisation de db.Text pour des descriptions longues

    def __init__(
        self,
        email,
        password,
        username=None,
        phone_number=None,
        profil_url=None,
        description=None,
    ):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.profil_url = profil_url
        self.description = description


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(225), nullable=False, unique=True)

    def __init__(self, token):
        self.token = token


def init_db():
    db.drop_all()
    db.create_all()
    user_1 = User(
        username="djefferson",
        email="tsafackjefferson@gmail.com",
        phone_number="4502727808",
        password="tsd1223",
    )
    user_2 = User(
        username="djeff",
        email="tsafack@gmail.com",
        phone_number="4502727708",
        password="tsd1227",
    )
    user_3 = User(
        username="tsafack",
        email="tsafack456@gmail.com",
        phone_number="4502727709",
        password="tsd1225",
    )

    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)

    db.session.commit()
    lg.warning("database initialized!")
