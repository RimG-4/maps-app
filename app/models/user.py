from app.utils.db import db

class T_User(db.Model):
    __tablename__ = 'T_User'
    userID = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    trips = db.relationship('T_TripHistory', back_populates='user')
