from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class T_User(db.Model):
    __tablename__ = 't_user'
    userID = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    trips = db.relationship('T_TripHistory', back_populates='user')
