from app.utils.db import db

class T_TrafficData(db.Model):
    __tablename__ = 'T_TrafficData'
    dataID = db.Column(db.Integer, primary_key=True)
    routeID = db.Column(db.Integer, db.ForeignKey('T_Route.routeID'))
    trafficStatus = db.Column(db.String, nullable=False)
    accidents = db.Column(db.String, nullable=True)

    route = db.relationship('T_Route', back_populates='traffic')
