from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.db import db


class T_User(db.Model, UserMixin):
    __tablename__ = 'T_User'

    userID = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    trips = db.relationship('T_TripHistory', back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.userID)  # важно для Flask-Login

    def __repr__(self):
        return f"<User {self.login}>"
