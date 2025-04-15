from flask_login import UserMixin
from app.utils.db import db
from app import login_manager

class T_User(db.Model, UserMixin):
    __tablename__ = 'T_User'
    userID = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    trips = db.relationship('T_TripHistory', back_populates='user')

@login_manager.user_loader
def load_user(user_id):
    return T_User.query.get(int(user_id))