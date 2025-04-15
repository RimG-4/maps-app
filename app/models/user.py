from flask_login import UserMixin
from app.utils.db import db

class T_User(db.Model, UserMixin):
    __tablename__ = 'T_User'
    userID = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    trips = db.relationship('T_TripHistory', back_populates='user')

    def __repr__(self):
        return f"<User {self.login}>"
