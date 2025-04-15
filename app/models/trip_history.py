from app.utils.db import db

class T_TripHistory(db.Model):
    __tablename__ = 'T_TripHistory'
    tripID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('T_User.userID'))
    routeID = db.Column(db.Integer, db.ForeignKey('T_Route.routeID'))
    dataTaken = db.Column(db.DateTime, nullable=False)

    user = db.relationship('T_User', back_populates='trips')
    route = db.relationship('T_Route', back_populates='trips')
